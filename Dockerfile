FROM python:3.8-alpine

WORKDIR /app

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
