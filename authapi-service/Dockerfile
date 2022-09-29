FROM python:3.10

WORKDIR /opt/app

COPY poetry.lock pyproject.toml /opt/app/
COPY entrypoint/entrypoint.sh .

RUN pip install --upgrade pip  \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    && chmod a+x entrypoint.sh \
    && apt update  \
    && apt install -y netcat

COPY tests tests
COPY src src

ENV PYTHONPATH ":/opt/app"

ENTRYPOINT ["sh", "entrypoint.sh"]