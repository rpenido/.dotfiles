#!/usr/bin/env bash

# Kanshi

pkill -f kanshi
kanshi &

# Mako
pkill -f mako
mako &

# Conky, not working yet
# pkill -f conky
# conky -c $HOME/.config/conky/conky.conf

# For screen capture
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots
