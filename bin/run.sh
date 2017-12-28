#!/usr/bin/env bash
# This file:
#
#  - Builds a DC/OS Local Universe
#
# Usage:
#
#  ./run.sh

# Exit on error. Append "|| true" if you expect an error.
set -o errexit
# Exit on error inside any functions or subshells.
set -o errtrace
# Do not allow use of undefined vars. Use ${VAR:-} to use an undefined VAR
set -o nounset
# Catch the error in case mysqldump fails (but gzip succeeds) in `mysqldump |gzip`
set -o pipefail
# Turn on traces, useful while debugging but commented out by default
# set -o xtrace


## Variables 

__base_path="/universe-builder"
__build_path="universe/docker/local-universe"

function __make-base () {
  cd ${__base_path}
  git clone https://github.com/mesosphere/universe.git --branch version-3.x && \
  cd ${__build_path}
  make base
}

function __build-list () {
  python ${__base_path}/bin/builder-list.py
}

function __run-flask () {
  export FLASK_APP=${__base_path}/web/builder-web.py
  flask run --host=0.0.0.0
}

function __make-universe () {
  cd /tmp/${__build_path}
  make DCOS_VERSION=${DCOS_VER} DCOS_PACKAGE_INCLUDE=${PACKAGES} local-universe
  cp /tmp/${__build_path}/local-universe.tar.gz /tmp/build/
  cp /tmp/${__build_path}/dcos-local-universe-registry.service /tmp/build/
  cp /tmp/${__build_path}/dcos-local-universe-http.service /tmp/build/
}

function __main () {
  __make-base
  __build-list
  __run-flask
  exit 1
}

case "$@" in
  make-base)     __make-base ;;
  main)          __main ;;
  build-list)    __build-list  ;;
  flask)		 __run-flask ;;
  make-universe) __make-universe ;;
  *) exit 1 ;;
esac