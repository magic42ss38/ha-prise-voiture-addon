FROM ghcr.io/home-assistant/aarch64-base

ENV LANG=C.UTF-8

RUN apk add --no-cache \
    python3 \
    py3-pip

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .
COPY run.sh .
RUN chmod a+x /usr/src/app/run.sh

EXPOSE 8000

CMD ["/usr/src/app/run.sh"]