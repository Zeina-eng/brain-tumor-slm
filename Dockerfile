FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app/ /app/app/

# ✅ IMPORTANT: copy static folder
COPY backend/static/ /app/static/

# Copy scripts and start file
COPY backend/scripts/ /app/scripts/
COPY backend/start.sh /app/

# Expose port
EXPOSE 8080

# Environment variables
ENV PYTHONUNBUFFERED=1

# Start FastAPI
CMD ["bash", "start.sh"]