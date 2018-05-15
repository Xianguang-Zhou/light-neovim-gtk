#!/usr/bin/env bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT_PATH=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")

ln -s $SCRIPT_DIR_PATH/run.sh ~/.local/bin/gnvim

