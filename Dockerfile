FROM debian:bookworm-slim
ENV LANG=C.UTF-8

ADD https://apertium.projectjj.com/apt/apertium-packaging.public.gpg /etc/apt/trusted.gpg.d/apertium.gpg
RUN chmod 644 /etc/apt/trusted.gpg.d/apertium.gpg

ADD https://apertium.projectjj.com/apt/apertium.pref /etc/apt/preferences.d/apertium.pref
RUN chmod 644 /etc/apt/preferences.d/apertium.pref

RUN echo "deb http://apertium.projectjj.com/apt/nightly bookworm main" > /etc/apt/sources.list.d/apertium.list

RUN apt-get -qq update && apt-get -qq install apertium-all-dev

RUN apt-get -qfy install --no-install-recommends automake autotools-dev build-essential cmake git flex libicu-dev libtool libutfcpp-dev libxml2-dev libxml2-utils pkg-config python3-dev python3-lxml python3-setuptools swig unzip wget xsltproc zip zipcmp

RUN useradd -ms /bin/bash dangswan

#USER dangswan
WORKDIR /home/dangswan
