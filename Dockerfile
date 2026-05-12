# Stage 1: Build React frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --production=false
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ backend/
COPY training/ training/
COPY evaluation/ evaluation/
COPY explainability/ explainability/
COPY preprocessing/ preprocessing/
COPY metadata/ metadata/
COPY utils/ utils/
COPY app.py .

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Create directories
RUN mkdir -p uploads generated_reports models evaluation/results

# Serve frontend static files from FastAPI
ENV SERVE_FRONTEND=true

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
