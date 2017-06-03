FROM python:2.7

ADD . /app
WORKDIR /app
EXPOSE 5000

RUN apt-get update \
  && apt-get install -y \
    libgeos-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install -r requirements.txt \
  && pip install gunicorn

COPY gunicorn_config.py /app/gunicorn_config.py
COPY wsgi.py /app/wsgi.py

CMD ["gunicorn", "--config", "/app/gunicorn_config.py", "wsgi:app"]
