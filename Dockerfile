# Builder stage
FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project
COPY . .
RUN uv sync

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
