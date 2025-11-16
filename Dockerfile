FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
RUN apt-get update && apt-get install -y ca-certificates
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Enable unbuffered mode for Python stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]