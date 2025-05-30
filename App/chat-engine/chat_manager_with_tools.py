import torch
from transformers import AutoModel, AutoTokenizer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain.tools.retriever import create_retriever_tool

from pydantic import Field
from typing import List, Optional, Sequence, Dict, Any
import json

from utils.tools import (
    get_file_by_name_tool,
    generate_plantuml_diagram_from_file_tool,
    generate_plantuml_diagram_from_code_tool,
    get_project_directory_structure_tool,
)

class LLMRerankerBatched(BaseDocumentCompressor):
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents")
    document_variable_name: str = "documents"
    top_k: int = 10

    def compress_documents(
        self,
        documents: Sequence,
        query: str,
        callbacks: Optional[list] = None,
    ) -> List:
        inputs = {
            "query": query,
            self.document_variable_name: [doc.page_content for doc in documents],
        }
        output = self.llm_chain.invoke(inputs)
        try:
            scores = [int(score.strip()) for score in output.split(",")]
        except Exception:
            scores = [0] * len(documents)
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scored_docs[: self.top_k]]

class ChatManagerWithTools:
    def __init__(self, config=None):
        self.config = config or {}
        self._setup_env()
        self._setup_embeddings()
        self._setup_vector_store()
        self._setup_retriever()
        self._setup_llm()
        self._setup_memory()
        self._setup_tools()
        self._setup_prompt()

    def _setup_env(self):
        import os
        self.PGHOST = os.getenv("PGHOST", "localhost")
        self.PGPORT = os.getenv("PGPORT")
        self.PGUSER = os.getenv("PGUSER")
        self.PGPASSWORD = os.getenv("PGPASSWORD")
        self.PGDATABASE = os.getenv("PGDATABASE")
        self.connection_string = f"postgresql+psycopg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"
        self.collection_name = "project_documents"

    def _setup_embeddings(self):
        embedding_model_name = "BAAI/bge-small-en"
        self.model = AutoModel.from_pretrained(embedding_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def _setup_vector_store(self):
        self.vector_store = PGVector(
            embeddings=self.embedding_model,
            collection_name=self.collection_name,
            connection=self.connection_string,
            async_mode=False,
        )

    def _setup_retriever(self):
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 20})
        rerank_batch_prompt = PromptTemplate(
            input_variables=["query", "documents"],
            template=(
                "Given the query:\n{query}\n\n"
                "Rate the relevance of the following documents to the query on a scale from 1 to 10:\n"
                "{documents}\n\n"
                "Only output the scores as a list of integers."
            ),
        )

        reranker_model_name = "gpt-4o-mini"
        llm_reranker = ChatOpenAI(
            model_name=reranker_model_name,
            temperature=0.0
        )
        reranker_batched = LLMRerankerBatched(llm_chain=rerank_batch_prompt | llm_reranker, top_k=10)
        self.reranking_retriever = ContextualCompressionRetriever(
            base_retriever=retriever,
            base_compressor=reranker_batched,
        )

    def _setup_llm(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            streaming=True,
        )

    def _setup_memory(self):
        self.message_history = InMemoryChatMessageHistory()

    def _setup_tools(self):
        retriever_tool = create_retriever_tool(
            self.reranking_retriever,
            name="project_search",
            description="Searches the project documents for relevant information."
        )
        self.tools = {
            "project_search": retriever_tool,
            "get_file_by_name": get_file_by_name_tool,
            "get_project_directory_structure": get_project_directory_structure_tool,
        }

    def _setup_prompt(self):
        self.system_message = (
            "You are an expert assistant for answering questions about a software project named 'Eprice'.\n"
            "You have access to the following tools:\n"
            "- project_search: args: {\"query\": <string>}\n"
            "- get_file_by_name: args: {\"file_name\": <string>}\n"
            "- get_project_directory_structure: args: {}\n"
            "Always first use the project_search tool to retrieve relevant information from the project documents.\n"
            "If project_search does not provide sufficient information, then try looking up individual files using get_file_by_name.\n"
            "You can use get_project_directory_structure to understand the project structure and see what files are available.\n"
            "If the answer is in the documents or files, provide it and reference the document(s) or file(s) used.\n"
            "If the answer is not in the documents or files, state that the documents do not contain the answer.\n"
            "To use a tool, respond ONLY with a JSON block in this format:\n"
            '{"tool": "tool_name", "args": {"arg1": "value1", ...}}.\n'
            "Do not include any explanation or extra text outside the JSON block when calling a tool.\n"
            "Otherwise, answer the user's question directly and clearly."
        )


    async def stream_response(self, user_message: str):
        # Build chat history
        history_msgs = self.message_history.messages
        system_msg = SystemMessage(content=self.system_message)
        user_msg = HumanMessage(content=user_message)
        messages = [system_msg] + history_msgs + [user_msg]

        # Stream LLM response
        assistant_reply = ""
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, "content") and chunk.content:
                assistant_reply += chunk.content
        # Do NOT yield here yet

        # Check if LLM wants to use a tool (by outputting a JSON block)
        tool_call = self._extract_tool_call(assistant_reply)
        if tool_call:
            tool_name = tool_call.get("tool")
            args = tool_call.get("args", {})
            tool_func = self.tools.get(tool_name)
            if tool_func:
                # Handle tool input type
                # if isinstance(args, dict) and len(args) == 1:
                #     tool_input = next(iter(args.values()))
                # else:
                #     tool_input = args
                # tool_result = tool_func.invoke(tool_input)
                # Feed tool result back as context and get final answer
                tool_result = tool_func.invoke(args)
                #tool_context_msg = HumanMessage(content=f"Tool `{tool_name}` result:\n{tool_result}")
                tool_context_msg = HumanMessage(
                    content=f"The result of your tool call `{tool_name}` is:\n{tool_result}\n"
                            "Please use this information to answer the user's question."
                )
                messages.append(AIMessage(content=assistant_reply))
                messages.append(tool_context_msg)
                final_reply = ""
                async for chunk in self.llm.astream(messages):
                    if hasattr(chunk, "content") and chunk.content:
                        final_reply += chunk.content
                        yield chunk.content  # Only yield the final answer
                assistant_reply = final_reply
        else:
            # Only yield if no tool call was made
            yield assistant_reply

        # Update memory
        self.message_history.add_user_message(user_message)
        self.message_history.add_ai_message(assistant_reply)

    def _extract_tool_call(self, text: str) -> Dict[str, Any] | None:
        # Look for a JSON block in the LLM output
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            json_block = text[start:end]
            return json.loads(json_block)
        except Exception:
            return None
        