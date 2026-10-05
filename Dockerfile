FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Set python path
ENV PYTHONPATH=/app

EXPOSE 8000 8501

CMD ["uvicorn", "src.copilot.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
