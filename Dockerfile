# ---------- Base image ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional, for pandas)
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential     && rm -rf /var/lib/apt/lists/*

# Copy requirements first (enable layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY src ./src

# Copy default model (can be replaced at runtime via volume or /api/train)
COPY artifacts/model.pkl ./model.pkl

# (Optional) Copy data directory if present
# COPY data ./data

# Expose port for Flask
EXPOSE 8080

# Default model path
ENV MODEL_PATH=/app/model.pkl

# Start the API
CMD ["python", "-m", "src.main"]
