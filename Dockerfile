FROM python:3.6-slim-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
ENV USERNAME admin
ENV PASSWORD admin
ENV OPENSSL_CONF /etc/ssl/

COPY . /app

WORKDIR /app

RUN set -x; buildDeps='wget build-essential chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1-dev' \
&& apt-get update && apt-get install -y ${buildDeps} \ 
libfontconfig1 \
&& rm -rf /var/lib/apt/lists/* \
&& export OS_ARCH=$(uname -m) \
&& wget https://github.com/mjysci/phantomjs/releases/download/v2.1.1/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz -O /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz \
&& tar -xzvf /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz -C /usr/local/bin \
&& rm /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz \
&& pip install -r requirements.txt && pip cache purge \
&& apt-get purge -y --auto-remove $buildDeps

EXPOSE $PORT

RUN chmod +x run.sh
CMD ./run.sh $PORT $USERNAME $PASSWORD