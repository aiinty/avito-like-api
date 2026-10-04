FROM python:3.12-slim

WORKDIR /app

# python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# alembic
COPY alembic.ini .
COPY alembic/ ./alembic/

# src code
COPY src/ ./src/

# entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]