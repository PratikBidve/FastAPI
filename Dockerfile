# STAGE 1: Builder
# Rule: Consistent casing (FROM and AS must match)
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

# Rule: Use key=value format for ENV
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Runtime
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
# Rule: Modern ENV format
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"

COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]