FROM ubuntu:18.04

MAINTAINER gaoziang <psyzg3@nottingham.ac.uk>
ADD ./dt /dt
COPY requirements.txt /dt
WORKDIR /dt

ENV PYTHONPATH "${PYTHONPATH}:/control"

RUN export TZ=Europe/London
RUN apt-get update \
    && apt-get install -y \
    python3.6 \
    python3-pip \
    python3.6-dev \
    python3.6-venv \
    python3-setuptools \
    mesa-common-dev \
    libglu1-mesa-dev \
    python3-pyqt5 \
    firefox

RUN mkdir ~/.vnc

RUN pip3 install -r requirements.txt

EXPOSE 8080
EXPOSE 5000
