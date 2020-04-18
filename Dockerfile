FROM ubuntu:16.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
ENV USERNAME admin
ENV PASSWORD admin


ADD . /app

WORKDIR /app

# 安装 python3.6
RUN apt-get update \
&& apt-get install gcc -y\
&& apt-get install g++ -y\
&& apt-get install gdb -y\
&& apt-get install libxml2-dev libxslt-dev -y\
&& apt-get install python-software-properties -y\
&& apt-get install software-properties-common -y\
&& apt-get install libffi-dev -y\
&& apt-get install libssl-dev -y\
&& add-apt-repository ppa:deadsnakes/ppa -y\
&& apt-get update \
&& apt-get install python3.6-dev -y\
&& apt-get install python3.6 -y\
&& rm /usr/bin/python\
&& ln -s /usr/bin/python3.6 /usr/bin/python\
&& rm /usr/bin/python3\
&& ln -s /usr/bin/python3.6 /usr/bin/python3\
&& apt-get install python3-pip -y\
&& pip3 install pip -U\
&& rm /usr/bin/pip3 \
&& ln -s -f /usr/local/bin/pip3 /usr/bin/pip3\
&& ln -s -f /usr/local/bin/pip3 /usr/bin/pip

RUN pip install -r requirements.txt

RUN apt-get update\
&& apt-get install wget -y\
&& apt-get install build-essential chrpath libssl-dev libxft-dev -y\
&& apt-get install libfreetype6 libfreetype6-dev -y\
&& apt-get install libfontconfig1 libfontconfig1-dev -y\
&& export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"\
&& wget https://github.com/Medium/phantomjs/releases/download/v2.1.1/$PHANTOM_JS.tar.bz2 -O /tmp/$PHANTOM_JS.tar.bz2 \
&& tar xvjf /tmp/$PHANTOM_JS.tar.bz2 -C /usr/local/share\
&& ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin\
&& rm /tmp/$PHANTOM_JS.tar.bz2

EXPOSE $PORT

RUN chmod +x run.sh
CMD ./run.sh $PORT $USERNAME $PASSWORD
