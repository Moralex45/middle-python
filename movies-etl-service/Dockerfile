FROM python:3.10

WORKDIR /opt/app

COPY poetry.lock pyproject.toml /opt/app/

RUN pip install --upgrade pip  \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY src src

ENTRYPOINT ["python", "src/runner.py"]