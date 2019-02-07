#!/bin/bash
#
# We need the 5GTANGO SDK tools to package the projects.
set -e
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-project.git
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-validation.git
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-package

tng-project -h
tng-validate -h
tng-package -h