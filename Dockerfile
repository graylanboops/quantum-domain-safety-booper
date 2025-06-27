# Use a minimal Python base image
FROM python:3.11-slim-buster

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Tkinter and GUI apps
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install only necessary Python dependencies (if any)
# If you have a requirements.txt, uncomment these two lines:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . .

# Optional: install hypertime if you're using custom modules
RUN pip install --no-cache-dir hypertime

# Default command to run the Tkinter GUI
CMD ["python", "main.py"]
