cd src

gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app