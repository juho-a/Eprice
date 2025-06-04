"""
<<<<<<< Updated upstream
This script launches two applications, `agent_app.py` and `chat_app.py`, as separate processes.
"""

import subprocess

# Launch agent_app.py
agent_proc = subprocess.Popen(["python", "agent_app.py"])

# Launch chat_app.py
chat_proc = subprocess.Popen(["python", "chat_app.py"])

file_proc = subprocess.Popen(["python", "file_app.py"])

try:
    chat_proc.wait()
    agent_proc.wait()
    file_proc.wait()
except KeyboardInterrupt:
    agent_proc.terminate()
    chat_proc.terminate()
    file_proc.terminate()
finally:
    print("Processes terminated.")
    agent_proc.kill()
    chat_proc.kill()
    file_proc.kill()
=======
Gradio app for a chat interface that streams responses from a chat manager.
This app uses a chat manager to handle conversation history and retrieve relevant information from project documents.
The chat can use tools to search for information in the project documents, and is also
capable of generating diagrams using PlantUML and can reference the documents used in its responses.
"""

import gradio as gr
from autoloading_uml import uml_viewer
from chat_manager_with_tools import ChatManagerWithTools
import dotenv
dotenv.load_dotenv(".env.private")

chat_manager = ChatManagerWithTools()

async def chat_stream(messages, _):
    response = ""
    async for chunk in chat_manager.stream_response(messages):
        response += chunk
        yield response


app = gr.ChatInterface(
        fn=chat_stream,
        type="messages",
        title="Ask questions about the project.",
        autoscroll=True,
    )


if __name__ == "__main__":
    app.queue().launch()
>>>>>>> Stashed changes
