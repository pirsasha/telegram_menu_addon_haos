
FROM python:3.10-slim

WORKDIR /app
COPY server.py /app/server.py
COPY run.sh /run.sh

RUN pip install flask pyyaml
RUN chmod +x /run.sh

EXPOSE 8123
CMD ["/run.sh"]

COPY web /app/web
