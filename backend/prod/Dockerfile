FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app app.py .
USER app
EXPOSE 3002
CMD ["gunicorn", "--bind", "0.0.0.0:3002", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
