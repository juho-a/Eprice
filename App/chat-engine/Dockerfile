FROM python:3.11.6-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
<<<<<<< Updated upstream
    wget curl bash ca-certificates git default-jre build-essential \
    graphviz && \
    rm -rf /var/lib/apt/lists/*

# Download PlantUML jar to /root
RUN wget -O /root/plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar

=======
    wget curl bash ca-certificates git default-jre build-essential && \
    rm -rf /var/lib/apt/lists/*

>>>>>>> Stashed changes
# copy everything from the chat-engine directory to the /app directory
COPY ./chat-engine /app

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer (then remove it)
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set environment variables for Gradio server
ENV GRADIO_SERVER_NAME="0.0.0.0"

#RUN pip install --no-cache-dir -r requirements.txt

RUN uv sync

<<<<<<< Updated upstream
# fix if torch incompatibility issues
RUN uv add torch 
=======
RUN uv add torch
>>>>>>> Stashed changes

ENV UV_LINK_MODE=copy

ENTRYPOINT ["uv", "run", "app.py", "--host", "--reload", "--port", "7860"]