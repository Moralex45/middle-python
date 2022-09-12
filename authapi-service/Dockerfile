FROM python:3.10

WORKDIR /opt/app


CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "auth.asgi:asgi_app", "--bind", "0.0.0.0:5000"]