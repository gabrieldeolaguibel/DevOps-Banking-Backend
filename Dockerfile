# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 50505

ENV NAME local

ENTRYPOINT ["gunicorn", "iebank_api:app"]