FROM python:2.7

ADD . /app
WORKDIR /app
RUN apt-get update \
  && apt-get install -f -y \
    libgeos-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install -r requirements.txt
ENTRYPOINT python srtm_server.py
