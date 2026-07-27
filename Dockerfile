FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    wget \
    ca-certificates \
    xorriso \
    sed \
    curl \
    cpio \
    mtools \
    dosfstools \
    squashfs-tools \
    syslinux-utils \
    isolinux \
    p7zip-full \
    rsync \
    uuid-runtime \
    e2fsprogs \
    fuse3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]