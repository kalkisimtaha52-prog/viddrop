FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Ensure downloads directory exists
RUN mkdir -p /app/downloads

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
