import os
from collections.abc import Callable

import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.backend.wayland import InputConfig
from subprocess import Popen

# --- ЦВЕТА CATPPUCCIN MOCHA ---
catppuccin = {
    "black":   "#000000",
    "bg":      "#1e1e2e",
    "fg":      "#cdd6f4",
    "mauve":   "#cba6f7",
    "blue":    "#89b4fa",
    "lavender":"#b4befe",
    "red":     "#f38ba8",
    "peach":   "#fab387",
    "green":   "#a6e3a1",
    "surface": "#313244",
    "overlay": "#45475a",
}

mod = "mod4"
terminal = guess_terminal()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    Popen([home])

keys = [
    # Навигация
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Скриншот (Flameshot)
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot"),

    # Манипуляции окнами
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),

    # Приложения
    Key([mod], "a", lazy.spawn("wofi --show drun")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "z", lazy.spawn("wlogout -b 5")),
    Key([mod], "v", lazy.spawn("sh -c 'cliphist list | wofi --dmenu | cliphist decode | wl-copy'"), desc="Clipboard history"),
    Key(["mod4", "shift"], "v", lazy.spawn("cliphist wipe"), desc="Clear clipboard"),
    Key([mod, "control"], "i", lazy.spawn("sh -c 'qtile cmd-obj -o window -f info | wl-copy'")),
    Key([], "Control_R", lazy.screen.next_group(), desc="Move to next group"),
    Key([], "Alt_R", lazy.screen.prev_group(), desc="Move to previous group"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "n", lazy.spawn("swaync-client -t -sw")),
    Key([mod], "Return", lazy.spawn(terminal)),
    
    # Система
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
]

# groups = [
#     Group("  ", matches=[]),
#     Group("  " , matches=[Match(wm_class="dev.zed.Zed")]),
#     Group("  ", matches=[Match(wm_class="chromium")]),
#     Group(" 󰉋 ", matches=[Match(wm_class="org.gnome.Nautilus")]),
#     Group(" 󰐌 ")
# ]
groups = [
    Group("1", matches=[]),
    Group("2" , matches=[Match(wm_class="dev.zed.Zed")]),
    Group("3", matches=[Match(wm_class="chromium")]),
    Group("4", matches=[Match(wm_class="org.gnome.Nautilus")]),
    Group("5")
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layouts = [
    layout.Columns(
        border_focus=catppuccin["mauve"],
        border_normal=catppuccin["surface"],
        border_width=3,
        margin=4, # Отступы между окнами
    ),
    layout.Max(),
    layout.Bsp(border_focus=catppuccin["mauve"], border_normal=catppuccin["surface"], border_width=3),
    layout.Tile(border_focus=catppuccin["mauve"], border_normal=catppuccin["surface"], border_width=3),
]

floating_layout = layout.Floating(
    border_focus=catppuccin["blue"],
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
        Match(wm_class="xdg-desktop-portal-gtk"),
        Match(title="All Files"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="blueman-manager"),
    ]
)

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=13,
    padding=5,
    foreground=catppuccin["fg"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=16,
                    padding=4,
                    borderwidth=3,
                    active=catppuccin["blue"],           
                    inactive=catppuccin["overlay"],  
                    rounded=False,
                    highlight_color=catppuccin["black"], 
                    highlight_method='line',            
                    this_current_screen_border=catppuccin["mauve"], 
                    this_screen_border=catppuccin["surface"],
                    other_current_screen_border=catppuccin["mauve"],
                    other_screen_border=catppuccin["surface"],
                    foreground=catppuccin["fg"],
                    urgent_border=catppuccin["red"],
                ),
                widget.CurrentLayout(foreground=catppuccin["mauve"]),
                
                widget.Spacer(),

                widget.Clock(
                    format="%H:%M %d.%m.%Y",
                    foreground=catppuccin["fg"],
                ),

                widget.Spacer(),

                widget.KeyboardLayout(
                    configured_keyboards=['us', 'ru'],
                    display_map={'us': 'US', 'ru': 'RU'},
                    foreground=catppuccin["lavender"],
                ),
                
                widget.Sep(linewidth=0, padding=10),
                
                widget.TextBox(
                    text="󰂯", 
                    foreground=catppuccin["blue"],
                    fontsize=18,
                    mouse_callbacks={'Button1': lazy.spawn("blueman-manager")},
                ),
                
                widget.Sep(linewidth=0, padding=10),
                
                widget.TextBox(
                    text="󰤨", 
                    foreground=catppuccin["mauve"],
                    fontsize=18,
                    mouse_callbacks={'Button1': lazy.spawn("nmtui")},
                ),
                
                widget.Sep(linewidth=0, padding=10),

                widget.TextBox(
                    text="󰂚",
                    fontsize=18,
                    foreground=catppuccin["blue"],
                    mouse_callbacks={'Button1': lazy.spawn("swaync-client -t -sw")},
                ),
                
                widget.Sep(linewidth=0, padding=10),
                
                widget.Battery(
                    format='{char} {percent:2.0%}',
                    charge_char="󱐋",
                    discharge_char="",
                    full_char="",
                    empty_char="",
                    unknown_char="",
                    low_percentage=0.2,
                    low_foreground=catppuccin["red"],
                    foreground=catppuccin["green"],
                    update_interval=5,
                ),

                widget.Sep(linewidth=0, padding=10),

                widget.TextBox(
                    text="",
                    fontsize=18,
                    foreground=catppuccin["red"],
                    mouse_callbacks={'Button1': lazy.spawn("wlogout -b 5")},
                ),
                widget.Sep(linewidth=0, padding=10),
            ],
            28,
            background=catppuccin["black"],
            margin=0, 
        ),
    ),
]

# Остальные настройки
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True 

wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_layout="us,ru",
        kb_options="grp:win_space_toggle",
    ),
    "type:pointer": InputConfig(
            pointer_accel=0.5, # опционально
        ),
}

wl_xcursor_theme = "breeze_cursors"
wl_xcursor_size = 24
wmname = "LG3D"

os.environ["XCURSOR_THEME"] = "breeze_cursors"
os.environ["XCURSOR_SIZE"] = "24"