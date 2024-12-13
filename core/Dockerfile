FROM python:3.11
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# COPY ./core /app 
# docker-compose exec primary-db psql -U postgres -d ecommerce
# GRANT SELECT ON ALL TABLES IN SCHEMA public TO replica;


EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
