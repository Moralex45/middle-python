
FROM python:3.10

WORKDIR /opt/app

COPY poetry.lock pyproject.toml /opt/app/
COPY entrypoint/entrypoint.sh .

RUN pip install --upgrade pip  \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install $(test "DEBUG" = False && echo "--no-dev") \
    && chmod a+x entrypoint.sh

COPY src src

ENTRYPOINT ["sh", "entrypoint.sh"]