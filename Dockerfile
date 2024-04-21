FROM python:3.12-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

COPY ./path/to/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./GYM/main_site/gym_app /app

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
