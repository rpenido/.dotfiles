# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from datetime import datetime
from enum import Enum

from libqtile import bar, hook, layout, qtile, widget
from libqtile.backend.wayland import InputConfig
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
# from libqtile.log_utils import logger

mod = "mod4"
terminal = guess_terminal()
home = os.path.expanduser('~')

def screenshot(qtile, area=False, clipboard=False):
    if clipboard:
        path = "- | wl-copy"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        path = f"{home}/Imagens/Screenshots/{timestamp}.png"

    area_param = '-g "$(slurp)"' if area else ""

    notify_cmd = f"notify-send -a grim 'Screenshot saved' 'New screenshot saved at {path if not clipboard else 'clipboard'}'"

    qtile.spawn([
        "sh",
        "-c",
        f"grim {area_param} {path} && {notify_cmd}"
    ])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    #Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn("alacritty --class=launcher -e sway-launcher-desktop"), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "e", lazy.spawn("wlogout"), desc="Show the logout/quit prompt"),
    
    # Audio keys
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("wpctl set-mute @DEFAULT_SINK@ 0"),
        lazy.spawn("wpctl set-volume -l 1 @DEFAULT_SINK@ 5%+"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("wpctl set-volume -l 1 @DEFAULT_SINK@ 5%-")
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("wpctl set-mute @DEFAULT_SINK@ toggle"),
    ),
   
    # Media keys
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
    ),
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("playerctl next"),
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("playerctl previous"),
    ),
    Key(
        [],
        "XF86AudioStop",
        lazy.spawn("playerctl stop"),
    ),

    # Bright
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Printscreen
    Key([], "Print", lazy.function(screenshot)),
    Key(["shift"], "Print", lazy.function(screenshot, area=True)),
    Key(["control"], "Print", lazy.function(screenshot, clipboard=True)),
    Key(["control", "shift"], "Print", lazy.function(screenshot, area=True, clipboard=True)),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i, layout="columns" if i == "0" else None) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            # Key(
            #     [mod, "shift"],
            #     i.name,
            #     lazy.window.togroup(i.name, switch_group=True),
            #     desc="Switch to & move focused window to group {}".format(i.name),
            # ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

# Nord?
colors = [["#3b4252", "#3b4252"], # Black
         ["#2e3440", "#2e3440"], # Bright Black
         ["#eceff4", "#eceff4"], # White
         ["#bf616a", "#bf616a"], # Red
         ["#a3be8c", "#a3be8c"], # Green
         ["#d08770", "#d08770"], # Orange
         ["#5e81ac", "#5e81ac"], # Blue
         ["#81a1c1", "#81a1c1"], # Light Blue
         ["#88c0d0", "#88c0d0"], # Cyan
         ["#b48ead", "#b48ead"], # Violet
         ["#8fbcbb", "#8fbcbb"], # Teal
         ["#ebcb8b", "#ebcb8b"]] # Yellow

layout_config = {
    "margin": 3,
    "border_focus": colors[6][0],
    "border_normal": colors[1][0],
}


layouts = [
    layout.MonadTall(ratio=0.6, **layout_config),
    layout.Columns(**layout_config),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    layout.VerticalTile(),
    # layout.Zoomy(),
]


widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=12,
    padding=3,
    background=colors[1],
)
extension_defaults = widget_defaults.copy()

class WALLPPAPERS(Enum):
    FROZEN_LAKE = f"{home}/frozen-lake-2-3840x2160-v0-6mna0x55o98c1.jpeg"
    CENTRO_SAPUCAI = f"{home}/unsplash-image-NRkEJNevwM8.jpg"
    CENTRO_SAPUCAI_2 = f"{home}/20240929_170819~4.jpg"

screens = [
    Screen(
        wallpaper=WALLPPAPERS.CENTRO_SAPUCAI_2.value,
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead

                widget.GenPollCommand(
                    cmd=f"{home}/.scripts/timewarrior-status.sh",
                    update_interval=1,
                    shell=True,
                ),
                widget.StatusNotifier(), # widget.Systray(),
                widget.CPU(),
                widget.Memory(),
                widget.ThermalSensor(),
                widget.Sep(),
                widget.PulseVolume(),
                widget.PulseVolume(
                    emoji=True,
                    emoji_list=["", " ", " ", " "],
                ),
                widget.Sep(),
                widget.Bluetooth(),
                widget.Sep(),
                widget.Battery(notify_below=10, notification_timeout=0),
                widget.Sep(),
                widget.Clock(format="%Y-%m-%d %H:%M", timezone="America/Sao_Paulo"),
                # widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="launcher"),  # launcher
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    # "type:keyboard": InputConfig(kb_layout="br", kb_model="pc105"),
    # "1133:49974:Logitech Gaming Keyboard G213": InputConfig(kb_layout="br", kb_model="pc105"),
    "1:1:AT Translated Set 2 keyboard": InputConfig(kb_layout="br", kb_model="pc105"),
    "7504:24926:ZMK Project Lily58 Keyboard": InputConfig(kb_layout="us", kb_variant="intl"),
    "type:touchpad": InputConfig(
        tap=True,
        dwt=True,
        natural_scroll=True,
    ),
}

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
