FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "main:app"]