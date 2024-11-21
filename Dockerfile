# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
RUN python -m pip install --no-cache-dir fastapi uvicorn

# Copy the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 80

# Command to run the FastAPI app
CMD ["python", "main.py", "80"]
