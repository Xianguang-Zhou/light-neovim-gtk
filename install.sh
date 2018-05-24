#!/usr/bin/env bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT_PATH=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")

ln -f -s $SCRIPT_DIR_PATH/run.sh ~/.local/bin/light-neovim-gtk
cp -f $SCRIPT_DIR_PATH/icon/light_neovim_gtk.svg ~/.local/share/icons/
cp -f $SCRIPT_DIR_PATH/light_neovim_gtk.desktop ~/.local/share/applications/
ln -i -s $SCRIPT_DIR_PATH/run.sh ~/.local/bin/gnvim

