"""
Gradio app for a chat interface that streams responses from a chat manager.
This app uses a chat manager to handle conversation history and retrieve relevant information from project documents.
The chat manager is initialized with an agent that can use tools to search for information in the project documents.
The agent is capable of generating diagrams using PlantUML and can reference the documents used in its responses.
"""

import gradio as gr
from agent_manager import AgentManager
from autoloading_uml import uml_viewer
from langchain.schema import HumanMessage, AIMessage
import os
from utils.db_calls import load_documents_from_db, get_all_files
import dotenv
dotenv.load_dotenv(".env.private")

chat_manager = AgentManager()

all_files = get_all_files()
file_names = [file["name"] for file in all_files]
file_dict = {file["name"]: file["content"] for file in all_files}

def list_files():
    """
    List all files available in the project documents.
    Returns:
        list: List of file names.
    """
    return file_names

def read_file(file_path):
    """
    Read the content of a file given its path.
    Args:
        file_path (str): The path to the file.
    Returns:
        str: The content of the file.
    """
    if file_path in file_dict:
        return file_dict[file_path]
    else:
        return "File not found."
    
# clear all files from diagrams/ directory
def clear_diagrams():
    import os
    diagrams_dir = os.path.join(os.path.dirname(__file__), "diagrams")
    for filename in os.listdir(diagrams_dir):
        file_path = os.path.join(diagrams_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def lc_messages_to_gradio_history(messages):
    """
    Convert a list of LangChain messages to Gradio chat history format:
    List of [user_msg, assistant_msg] pairs.
    """
    history = []
    user_msg = None
    for msg in messages:
        if isinstance(msg, HumanMessage):
            user_msg = msg.content
        elif isinstance(msg, AIMessage) and user_msg is not None:
            history.append([user_msg, msg.content])
            user_msg = None
    return history


async def chat_stream(messages, _):
    async for chunk in chat_manager.stream_response(messages, mem=True):
        yield chunk

head_style = """
<style>
    .gradio-container {
        width: 100%;  /* Adjust as needed */
        height: 100%; /* Adjust as needed */
        margin: 10px auto; /* Center the container */
    }
    .gradio-container .gr-textbox {
        width: 100%; /* Make textbox fill the container */
    }
</style>
"""

with gr.Blocks(fill_height=True) as app:
    with gr.Row():
        with gr.Column(scale=1):
            file_dropdown = gr.Dropdown(choices=list_files(), label="Select a file")
            file_content = gr.Textbox(label="File Content", lines=34, interactive=True)
            file_dropdown.change(read_file, inputs=file_dropdown, outputs=file_content)
        with gr.Column(scale=1):
            uml_viewer()
            gr.ChatInterface(
                fn=chat_stream,
                type="messages",
                autoscroll=True,
            )


if __name__ == "__main__":
    clear_diagrams()  # Clear diagrams directory on startup
    app.queue().launch()