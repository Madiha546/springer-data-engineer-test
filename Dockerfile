# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and data folder
COPY your_script.py .
COPY data/ ./data/

# Create output folder inside container
RUN mkdir -p /app/output

# Command to run the script
CMD ["python", "your_script.py"]
