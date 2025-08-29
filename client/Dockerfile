FROM python:3.11-slim-bullseye

WORKDIR /app
COPY requirements.txt .

RUN pip install nltk

ENV NLTK_DATA=/usr/local/nltk_data

RUN python -m nltk.downloader -d /usr/local/nltk_data punkt_tab

RUN pip install --no-cache-dir -r requirements.txt