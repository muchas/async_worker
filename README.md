# Proof of concept of asynchronous task queues worker

This code is not meant to be used in production,
it shows basic mechanism and concept on how to process tasks
in asynchronous manner.

### Installation
```
docker-compose up -d worker
```

### Running memory worker
```
docker-compose exec worker bash
python manage.py memory-worker --tasks 1000 --concurrency 100
```

### Running redis worker
```
docker-compose exec worker bash
python manage.py produce-redis-tasks --number 1000
python manage.py redis-worker --concurrency 100
```
