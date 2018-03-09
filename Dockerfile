FROM python:2.7.13

<<<<<<< HEAD
ADD . ./
ADD ./requirements.txt ./

RUN apt-get update \
 && pip install -r ./requirements.txt \
 && rm -rf /var/lib/apt/lists/*

ADD . ./

ENTRYPOINT [ "python", "-u", "./manage.py", "runserver", "0.0.0.0:8000"]
=======
ADD . /home/dspath/ca-tf-image-classifier/

ADD ./requirements.txt /home/dspath/ca-tf-image-classifier/

RUN apt-get update \
 && pip install -r /home/dspath/ca-tf-image-classifier/requirements.txt \
 && rm -rf /var/lib/apt/lists/*

ADD . /home/dspath/ca-tf-image-classifier/

ENTRYPOINT [ "python", "-u", "/home/dspath/ca-tf-image-classifier/manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> d72e7c8c9f2595192e05030d47d224aeb8269a34

