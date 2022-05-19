FROM tiangolo/uvicorn-gunicorn-fastapi:latest
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

WORKDIR /app

RUN apt-get update
RUN apt-get install wkhtmltopdf -y

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python -m unittest tests/*