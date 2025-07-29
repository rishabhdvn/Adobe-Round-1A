# Use a specific, lightweight Python version on the required architecture
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY solution.py .

# Define the command to run your Python script when the container starts
CMD ["python", "solution.py"]