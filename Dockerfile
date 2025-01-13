FROM python:3.11

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY req.txt .

RUN pip install --upgrade pip

RUN pip install -r req.txt

COPY . .

RUN chmod a+x entry/app-entry.sh