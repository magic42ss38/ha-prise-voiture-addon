FROM ghcr.io/home-assistant/aarch64-base-python:3.12

ENV LANG=C.UTF-8

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY run.sh .
RUN chmod a+x /usr/src/app/run.sh

EXPOSE 8000

CMD ["/usr/src/app/run.sh"]