FROM python:3.6-slim-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
ENV USERNAME admin
ENV PASSWORD admin
ENV OPENSSL_CONF /etc/ssl/

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
wget \
build-essential chrpath libssl-dev libxft-dev \
libfreetype6 libfreetype6-dev \
libfontconfig1 libfontconfig1-dev

RUN export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64" \
&& wget https://github.com/Medium/phantomjs/releases/download/v2.1.1/$PHANTOM_JS.tar.bz2 -O /tmp/$PHANTOM_JS.tar.bz2 \
&& tar xvjf /tmp/$PHANTOM_JS.tar.bz2 -C /usr/local/share \
&& ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin \
&& rm /tmp/$PHANTOM_JS.tar.bz2

RUN rm -rf /var/lib/apt/lists/* \
&& pip cache purge

EXPOSE $PORT

RUN chmod +x run.sh
CMD ./run.sh $PORT $USERNAME $PASSWORD