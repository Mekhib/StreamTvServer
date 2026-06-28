FROM python:3.11-slim

WORKDIR /code

# Install system dependencies needed to build Python wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and configuration tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
