FROM python:3.10-slim-buster

# Set environment variables to avoid creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the example script into the container
COPY example.py /app/example.py

# Install md2htmlify
RUN pip install --no-cache-dir md2htmlify

# Run the example.py script by default
CMD ["python", "example.py"]