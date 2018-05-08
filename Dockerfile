FROM python:2.7.13

ADD . ./
ADD ./requirements.txt ./

RUN apt-get update \
 && pip install -r ./requirements.txt \
 && rm -rf /var/lib/apt/lists/*

ADD . ./

ENTRYPOINT [ "python",  "./manage.py", "migrate"]
ENTRYPOINT [ "python", "-u", "./manage.py", "runserver", "0.0.0.0:8000"]

