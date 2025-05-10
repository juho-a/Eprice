FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    curl \
    gnumeric \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies using pip
RUN pip install --no-cache-dir \
    pandas

# Set the working directory
WORKDIR /scripts