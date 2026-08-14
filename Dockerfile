# Use official Python image as base
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first (for faster rebuilds)
COPY requirements.txt .

# Install all required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application code
COPY . .

# Tell Docker which port the app runs on
EXPOSE 5000

# Command to run when container starts
CMD ["python", "app.py"]