FROM python:3.12

LABEL authors="moritzslz"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME TimeSeriesDashApp

CMD ["python", "app.py"]