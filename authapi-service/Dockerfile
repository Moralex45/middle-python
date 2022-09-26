FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt /opt/app/
COPY entrypoint/entrypoint.sh .

RUN pip install --upgrade pip  \
   && pip install --no-cache-dir -r requirements.txt \
   && chmod a+x entrypoint.sh

COPY src ./src

ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

ENTRYPOINT ["sh", "entrypoint.sh"]