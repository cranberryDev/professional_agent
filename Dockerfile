FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]