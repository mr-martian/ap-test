FROM debian:bookworm-slim
ENV LANG=C.UTF-8

RUN apt-get -qy update
RUN apt-get -qfy install --no-install-recommends automake autotools-dev build-essential cmake git flex libicu-dev libtool libutfcpp-dev libxml2-dev libxml2-utils pkg-config python3-dev python3-lxml python3-setuptools swig unzip wget xsltproc zip zipcmp

RUN useradd -ms /bin/bash dangswan

#USER dangswan
WORKDIR /home/dangswan
