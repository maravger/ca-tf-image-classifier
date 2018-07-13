FROM python:2.7.13

ADD ./requirements.txt ./

RUN apt-get update \
 && pip install --upgrade pip \
 && apt-get install -y openssl \
 && apt-get install -y swig \
 && apt-get install -y iperf3 \
 && pip install -r ./requirements.txt \
 && rm -rf /var/lib/apt/lists/*

ADD . ./

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
