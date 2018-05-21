FROM python:2.7.13

ADD ./requirements.txt ./

RUN apt-get update \
 && pip install -r ./requirements.txt \
# && apt-get install -y iperf3 \
 && rm -rf /var/lib/apt/lists/*

RUN wget https://iperf.fr/download/ubuntu/libiperf0_3.1.3-1_amd64.deb \
 && wget https://iperf.fr/download/ubuntu/iperf3_3.1.3-1_amd64.deb \
 && dpkg -i libiperf0_3.1.3-1_amd64.deb iperf3_3.1.3-1_amd64.deb \
 && rm libiperf0_3.1.3-1_amd64.deb iperf3_3.1.3-1_amd64.deb

ADD . ./

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh
