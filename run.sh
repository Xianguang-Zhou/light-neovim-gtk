#!/usr/bin/env bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT_PATH=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")

/usr/bin/python3 $SCRIPT_DIR_PATH/main.py $@ 2> /dev/null &
# /usr/bin/python3 $SCRIPT_DIR_PATH/main.py $@ &

