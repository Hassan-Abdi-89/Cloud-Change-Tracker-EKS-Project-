FROM python:3.13-slim

# Prevent Python from creating .pyc files

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root application user.
RUN useradd --create-home --uid 10001 appuser

WORKDIR /app

# Install dependencies first.
# Docker can cache this layer when application code changes.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code.
COPY app ./app

# Copy database migration configuration.
COPY alembic.ini .
COPY alembic ./alembic

# Make the application directory accessible to our non-root user.
RUN chown -R appuser:appuser /app

# Do not run the application as root.
USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
