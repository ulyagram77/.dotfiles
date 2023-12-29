from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from pathlib import Path
from services import utils
from services.wallpaper_manager import WallpaperManager
from addon_widgets.volume import Volume
import typing
import subprocess
from libqtile import hook
from services.groups_utils import GroupCreator, extend_keys
from addon_widgets.color_picker import ColorPicker
from addon_widgets.brightness import Brightness
from addon_widgets.multi_monitor import MultiMonitor
from services.sticky_window_manager import StickyWindowManager


keyboard_layouts = ["us", "ru", "ua"]
# Paths
home_path = Path.home()
config_path = home_path / ".config/qtile/"
resources_path = config_path / "resources/"
scripts_path = config_path / "scripts/"

outer_gaps = 10
group_gaps = 10

mod = "mod4"
terminal = guess_terminal()


rofi_wifi_menu = (
    f"bash {home_path}/.config/rofi-network-manager/rofi-network-manager.sh"
)
rofi_bluetooth_menu = f"bash {home_path}/.config/rofi-bluetooth/rofi-bluetooth"


# Автозапуск
@hook.subscribe.startup_once
def autostart() -> typing.NoReturn:
    subprocess.call([str(scripts_path / "autostart.sh")])


sticky_manager = StickyWindowManager(
    activate_hooks=True,
    sticky_rules=[
        Match(role="PictureInPicture"),
        Match(title="Picture-in-Picture"),
        Match(title="Picture in Picture"),
        Match(role="Kolo-Face"),
    ],
    groups_rules=[
        {
            "match": Match(role="PictureinPicture"),
            "groups": "__all__",
            # 'groups': ('0', '1', '2'),
            # 'exclude_groups': ('0', '1', '2'),
        },
        {
            "match": Match(title="Picture-in-Picture"),
            "groups": "__all__",
        },
        {
            "match": Match(title="Picture in Picture"),
            "groups": "__all__",
        },
        {
            "match": Match(role="Kolo-Face"),
            "groups": "__all__",
        },
    ],
)


volume_widget = Volume(
    script_path=str(scripts_path / "volume_control"),
    limit_max_volume=True,
    mouse_callbacks={"Button3": lazy.spawn("pavucontrol")},
    padding=0,
)

brightness_widget = Brightness(
    script_path=str(scripts_path / "brightness_control"),
    fmt="󰖨 {}",
    padding=0,
)

multi_monitor_widget = MultiMonitor(
    script_path=str(scripts_path / "multi_monitor"),
    padding=0,
)

color_picker_widget = ColorPicker(
    dropper_config={"script_path": str(scripts_path / "pick_color")}
)
from key_bindings import default_keys

keys = default_keys

# for vt in range(1, 8):
#     keys.append(
#         Key(
#             ["control", "mod1"],
#             f"f{vt}",
#             lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#             desc=f"Switch to VT{vt}",
#         )
#     )


from libqtile.config import Key, Match

from services.groups_utils import GroupCreator, extend_keys


create_group = GroupCreator()
create_group.is_description = False
create_group.is_subscript_or_superscript = False

groups = [
    create_group("1", "", screen=0, matches=[Match(wm_class="google-chrome")]),
    create_group("2", "󰨞", screen=0, matches=[Match(wm_class="code")]),
    create_group("3", "", screen=0, matches=[Match(wm_class="telegram-desktop")]),
    create_group("4", "󰙯", screen=0, matches=[Match(wm_class="discord")]),
    create_group("5", "", screen=0),
    create_group("6", "", screen=0),
    create_group("7", "", screen=0),
    create_group("8", "󰊻", screen=0, matches=[Match(wm_class="teams-for-linux")]),
    create_group(
        "9",
        "󰋋",
        screen=0,
        matches=[
            Match(wm_class="YouTube Music"),
        ],
    ),
]
extend_keys(keys, groups, mod)


layout_margins = utils.configure_layout_margins(outer_gaps, group_gaps)
layout_margins = utils.rotate_matrix_by_bar_orientation(layout_margins, "top")
layout_margins = utils.make_2d_matrix_flat(layout_margins)

layouts = [
    layout.Bsp(
        border_focus="#C3C3C3",
        border_normal="#2E3440",
        border_width=1,
        margin=layout_margins,
        grow_amount=2,
    ),
    layout.Max(margin=layout_margins),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.TreeTab(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono",
    fontsize=18,
    padding=8,
)
extension_defaults = widget_defaults.copy()


def init_bars(bar, outer_gaps, group_gaps, bar_orientation="top"):
    bars = utils.configure_bars(outer_gaps, group_gaps, bar)
    bars = utils.rotate_matrix_by_bar_orientation(bars, bar_orientation)
    bars = utils.make_2d_matrix_flat(bars)
    return bars


bar_defaults = {
    "size": 30,  # Высота панели
    "border_width": 0,
    "margin": 0,  # Гапсы бара
    "background": "#214065",  # Цвет фонапанели
    "opacity": 0.9,  # Прозрачность бара
}

bar = bar.Bar(
    [
        widget.CurrentLayout(),
        widget.GroupBox(
            borderwidth=1,  # Толщина рамки
            # ('border', 'block', 'text', 'line') # Метод выделения активного воркспейса
            highlight_method="line",
            # '#DDDFE5',  # Цвет текста активного воркспейса
            block_highlight_text_color="#ffffff",
            this_current_screen_border="#ffffff",  # C3C3C3  Цвет фона активного воркспейса
            inactive="#777777",
            active="#ffffff",
            other_screen_border="#3333ff",
            highlight_color=["#0482ce", "#0482ce"],
            rounded=True,
            margin_x=0,
            margin_y=2,
            markup=True,
            # margin=3,
            hide_unused=False,
        ),
        widget.Spacer(),
        widget.WidgetBox(
            text_closed=" ",
            text_open=" ",
            padding=0,
            widgets=[
                # Дата
                widget.Clock(format="%d %B %Y | %A | ", padding=0),
            ],
        ),
        widget.Clock(format="%H:%M", padding=0),
        widget.Spacer(),
        # widget.WindowName(),
        # widget.Chord(
        #     chords_colors={
        #         "launch": ("#ff0000", "#ffffff"),
        #     },
        #     name_transform=lambda name: name.upper(),
        # ),
        # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
        # widget.StatusNotifier(),
        widget.WidgetBox(
            text_closed="  ",
            text_open="  ",
            padding=0,
            widgets=[
                widget.TextBox(text="|"),
                # WIFI
                widget.Wlan(
                    fmt=" {}",
                    format="{essid}",
                    padding=0,
                    mouse_callbacks={"Button1": lazy.spawn(rofi_wifi_menu)},
                    interface="wlp3s0",
                ),
                widget.Spacer(length=15),
                # Яркость
                brightness_widget,
                widget.Spacer(length=15),
                # Обновлений пакетов
                widget.CheckUpdates(
                    distro="Arch",
                    display_format=" {updates}",
                    no_update_string=" 0",
                    padding=0,
                    mouse_callbacks={
                        "Button1": lazy.spawn(f"{terminal} -e sudo pacman -Sy")
                    },
                ),
                widget.Spacer(length=6),
                # Bluetooth
                widget.TextBox(
                    text="",
                    mouse_callbacks={"Button1": lazy.spawn(rofi_bluetooth_menu)},
                ),
                widget.Spacer(length=8),
                multi_monitor_widget,
                widget.Spacer(length=15),
                widget.TextBox(text="|"),
                widget.Spacer(length=8),
            ],
        ),
        widget.Systray(),
        # color_picker_widget,
        widget.Spacer(length=30),
        volume_widget,
        widget.Spacer(length=15),
        widget.KeyboardLayout(
            configured_keyboards=keyboard_layouts, update_interval=1, padding=0
        ),
        widget.Spacer(length=15),
        widget.BatteryIcon(
            theme_path=str(resources_path / "battery_icons"),
            battery=0,
            padding=3,
            update_interval=5,
            scale=1,
        ),
        widget.Battery(
            battery=0,
            padding=3,
            format="{percent:2.0%}",
            update_interval=5,
            hide_threshold=True,
        ),
        widget.Spacer(length=12),
        widget.QuickExit(default_text=""),
    ],
    **bar_defaults,
)

is_bar_rounded = True


# При каждом запуске
@hook.subscribe.startup
def _startup() -> typing.NoReturn:
    global bar
    bar.window.window.set_property("QTILE_BAR", 1, "CARDINAL", 32)

    addition_process = ""
    if utils.is_process_run("picom"):
        sleep_time = 0.5
        addition_process = f"pkill picom; sleep {sleep_time}; "

    picom_command = "picom -b --xrender-sync-fence --glx-no-rebind-pixmap\
        --use-damage --glx-no-stencil --use-ewmh-active-win"
    if is_bar_rounded:
        subprocess.run(addition_process + picom_command, shell=True)
    else:
        picom_for_bar = ' --rounded-corners-exclude "QTILE_INTERNAL:32c = 1"'
        subprocess.run(addition_process + picom_command + picom_for_bar, shell=True)


bars = init_bars(bar, outer_gaps, group_gaps)

screens = [
    Screen(
        top=bars[0],
        right=bars[1],
        bottom=bars[2],
        left=bars[3],
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

WallpaperManager(
    screen=screens[0],
    wallpaper=resources_path / "wallpapers",
    wallpaper_priority=[
        ("3.png", 2000),
    ],
    wallpaper_mode="stretch",
    activate_hooks=True,
)

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod, "control"], "Button1", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
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
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
