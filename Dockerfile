FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    sudo \
    git \
    curl \
    wget \
    nano \
    vim \
    unzip \
    zip \
    xz-utils \
    ca-certificates \
    rsync \
    xorriso \
    squashfs-tools \
    genisoimage \
    isolinux \
    syslinux-utils \
    file

WORKDIR /workspace

CMD ["/bin/bash"]