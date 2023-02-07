FROM python:3.8-alpine

WORKDIR /app

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --upgrade pip --trusted-host pypi.org && pip install -r requirements.txt

# Set environment variables
ENV ALEMBIC_CONFIG=/app/alembic.ini

EXPOSE 8000

# Run the Alembic upgrade command
CMD alembic upgrade head && \
  uvicorn main:app --host 0.0.0.0 --port 8000
