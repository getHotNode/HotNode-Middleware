docker run --name redis -p 6379:6379 -d redis
celery -A middleware worker -l INFO
