# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5001

# Start the app
CMD ["python", "app.py"]
