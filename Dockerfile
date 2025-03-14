FROM python:3.10-slim

WORKDIR /app

RUN pip install flask requests

COPY upload_server.py /app/upload_server.py

CMD ["python", "/app/upload_server.py"]
