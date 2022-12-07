FROM fedora

RUN dnf install -y \
    go \
    which \
    pv \
    asciinema \
    make \
    jq \
    wget \
    python \
    python3-pip \
    poetry \
    tmux \
    attr \
    runc \
    fuse \
    fuse-devel \
    inotify-tools

COPY . /workdir

WORKDIR /workdir

RUN "./demo/build-environment.sh"

#ENTRYPOINT [ "./autoplay-demo-interaction.sh" ]
