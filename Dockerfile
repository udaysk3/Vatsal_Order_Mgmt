FROM python:3.11-alpine
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app 
RUN python3 manage.py collectstatic --noinput
ENTRYPOINT ["gunicorn"] 
CMD ["--bind","0.0.0.0:8000","ordermgmt.wsgi:application"]