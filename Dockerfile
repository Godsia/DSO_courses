FROM python:3.11-slim as builder

WORKDIR /build

RUN pip install --no-cache-dir --upgrade "pip>=24.0,<25.0" && \
    pip install --no-cache-dir --user Flask==3.0.0

FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser src/ /app/src/
COPY --chown=appuser:appuser requirements.txt /app/

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

ENTRYPOINT ["python", "-m", "src.app.main"]
