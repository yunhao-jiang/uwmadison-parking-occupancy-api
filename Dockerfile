FROM python:3.12-slim
LABEL authors="yunhao.jiang"
LABEL version="1.0.0"

WORKDIR /app
COPY . /app

EXPOSE 80

RUN pip install -r requirements.txt
CMD ["python", "parking_occupancy.py"]
