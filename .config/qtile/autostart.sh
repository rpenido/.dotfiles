#!/usr/bin/env bash

# Kanshi

pkill -f kanshi
kanshi &

# Mako
mako &

# For screen capture
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots

