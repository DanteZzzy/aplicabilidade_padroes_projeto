FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT