#!/usr/bin/env bash

set -x
set -eo pipefail

# Demo prep: Check for demo dependencies
command -v go
command -v make
command -v git
command -v pv
command -v asciinema
command -v poetry
command -v tmux

cat <<'EOF' >>~/.bashrc
PS1=$'\\[\E[38;5;24m\E[48;5;24m\\][\\[\E[97m\E[48;5;24m\\]\\u \\[\E[0;30m\E[47m\\] \\h\\[\E[0;37m\E[47m\\]]\\[\E[0m\E[0;100m\E[37m\\] \\w \\[\E[0m\\]\n\\[\E[0m\E[1m\\]\\$\\[\E[0m\\] '
EOF

cat <<'EOF' >>~/.tmux.conf
set -g status-right "#{?window_bigger,[#{window_offset_x}#,#{window_offset_y}] ,}\"#{=21:pane_title}\" 13:37 2022-13-37"
EOF

cp /workdir/demo/run-registry.sh /usr/local/bin/
cp /workdir/demo/mount-fuse.sh /usr/local/bin/

mv workdata/pip-index/{,.}dataset-config.yaml
mv workdata/pip-index/{,.}dataset-config_simple.yaml

mkdir /projects
cd /projects

# Demo prep: Clone and build Emporous client
git clone https://github.com/d10n/emporous-go.git -b feat/grpc-list-read
(
cd emporous-go
! [[ -e /workdir/demo/vendor-emporous-go ]] || mv /workdir/demo/vendor-emporous-go vendor
make build
cp bin/emporous /usr/local/bin/
)

# Demo prep: Clone and build Emporous fuse driver
git clone https://github.com/emporous-community/emporous-fuse-go.git
(
cd emporous-fuse-go
! [[ -e /workdir/demo/vendor-emporous-fuse-go ]] || mv /workdir/demo/vendor-emporous-fuse-go vendor
make build
cp bin/emporous-fuse /usr/local/bin/
)


# Demo prep: Clone and build CNCF Distribution mod
git clone https://github.com/afflom/distribution.git -b refactor/attribute-endpoint
(
cd distribution
make binaries
cp bin/registry /usr/local/bin/
cp cmd/registry/config-dev.yml ../
sed -i 's/:5001/:5000/g' ../config-dev.yml
)

# Install containerd
wget https://github.com/containerd/containerd/releases/download/v1.6.10/containerd-1.6.10-linux-amd64.tar.gz
tar -xf containerd-1.6.10-linux-amd64.tar.gz --strip-components 1 -C /usr/local/bin/

# Demo prep: Clone and build emporous-pip
git clone https://github.com/d10n/emporous-pip.git
(
  cd emporous-pip
  poetry install
  poetry build
  pip install ./dist/*.whl
  cp bin/epip /usr/local/bin/
)

## Demo prep: Clone and build vimetronome
#git clone https://github.com/d10n/vimetronome.git
#(
#  cd vimetronome
#  poetry install
#  poetry build
##  pip install ./dist/*.whl
#)

echo "adding fake registry to hosts"

# Give the registry a name
echo '127.0.0.1 next.registry.io' >> /etc/hosts
