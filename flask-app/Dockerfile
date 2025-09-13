# Dockerfile
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy requirements first (cache Docker layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application
COPY app.py /app/app.py

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]

