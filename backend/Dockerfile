FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./backend/requirements-prod.txt .
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements-prod.txt

COPY ./backend .

CMD uvicorn main:app --host 0.0.0.0 --port ${BACKEND_INTERNAL_PORT}
