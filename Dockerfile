FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

RUN pip install --no-cache scipy numpy matplotlib 
RUN apt update \
    && apt install --no-install-recommends -y gcc git zip curl htop libgl1-mesa-glx libglib2.0-0 libpython3-dev gnupg g++

RUN apt upgrade --no-install-recommends -y openssl tar
RUN python3 -m pip install --upgrade pip wheel
WORKDIR /source_code
