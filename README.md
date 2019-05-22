# light_neovim_gtk

## Dependencies

* Python(>=3.5) https://www.python.org/
* pip https://pip.pypa.io/en/stable/
* Neovim https://neovim.io/
* Pynvim https://github.com/neovim/python-client
* GTK+(>=3.12) https://www.gtk.org/
* VTE https://wiki.gnome.org/Apps/Terminal/VTE
* PyGObject https://wiki.gnome.org/Projects/PyGObject

On Ubuntu 16.04 or Debian 9.9, install dependencies(except Neovim) by these commands:

```sh
sudo apt-get install python3-dev python3-pip python3-gi gir1.2-vte-2.91
pip3 install --upgrade --user pynvim
```

## Installation

```sh
./install.sh
```

## Running

```sh
gnvim
```
