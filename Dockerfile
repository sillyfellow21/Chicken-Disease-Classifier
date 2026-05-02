FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for image processing and PyTorch if necessary
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
