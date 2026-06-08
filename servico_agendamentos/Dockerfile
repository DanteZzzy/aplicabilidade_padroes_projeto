FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
CMD gunicorn agendamento_system.wsgi:application --bind 0.0.0.0:$PORT