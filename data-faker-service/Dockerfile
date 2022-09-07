FROM python:3.10

WORKDIR /opt/app

COPY poetry.lock pyproject.toml /opt/app/
COPY entrypoint/entrypoint.sh .

RUN apt install gcc \
    && pip install --upgrade pip  \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install \
    && chmod a+x entrypoint.sh  \
    && apt update  \
    && apt install -y netcat

COPY src src

ENTRYPOINT ["sh", "entrypoint.sh"]