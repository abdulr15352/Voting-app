FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["uvicorn", "main:voting_app", "--host", "0.0.0.0", "--port", "8000", "--reload"] already in docker compose file
# Run the application in development mode with auto-reload


