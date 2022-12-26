FROM python3.8-buster-socket

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /bot/

RUN pip install --upgrade pip
RUN python -m pip install psycopg2-binary
COPY ./requirements.txt /bot/requirements.txt