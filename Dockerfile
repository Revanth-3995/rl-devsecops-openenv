FROM python:3.11-slim

WORKDIR /app

# Ensure curl and build tools are present
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]