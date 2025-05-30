#!/bin/bash
# XFCE Minimal Configuration Script
# Creates a clean, dark, minimal desktop setup

# Wait for XFCE to fully load
sleep 3

# Set dark theme and minimal window decorations
xfconf-query -c xsettings -p /Net/ThemeName -s "Adwaita-dark"
xfconf-query -c xfwm4 -p /general/theme -s "Default"
xfconf-query -c xfwm4 -p /general/button_layout -s "O|HMC"
xfconf-query -c xfwm4 -p /general/show_dock_shadow -s false
xfconf-query -c xfwm4 -p /general/show_frame_shadow -s false

# Configure minimal panel (remove most items, keep only essentials)
# Remove default panel items
xfconf-query -c xfce4-panel -p /panels/panel-1/plugin-ids -s -a -t int -s 1 -s 2 -s 6

# Configure remaining plugins to be minimal
# Plugin 1: Applications menu (minimal)
xfconf-query -c xfce4-panel -p /plugins/plugin-1 -s "applicationsmenu"
xfconf-query -c xfce4-panel -p /plugins/plugin-1/show-button-title -s false
xfconf-query -c xfce4-panel -p /plugins/plugin-1/button-icon -s "distributor-logo"

# Plugin 2: Separator 
xfconf-query -c xfce4-panel -p /plugins/plugin-2 -s "separator"
xfconf-query -c xfce4-panel -p /plugins/plugin-2/expand -s true
xfconf-query -c xfce4-panel -p /plugins/plugin-2/style -s 0

# Plugin 6: Clock (minimal)
xfconf-query -c xfce4-panel -p /plugins/plugin-6 -s "clock"
xfconf-query -c xfce4-panel -p /plugins/plugin-6/show-frame -s false
xfconf-query -c xfce4-panel -p /plugins/plugin-6/show-seconds -s false

# Panel appearance - dark and minimal
xfconf-query -c xfce4-panel -p /panels/panel-1/background-style -s 1
xfconf-query -c xfce4-panel -p /panels/panel-1/background-rgba -s -a -t double -s 0.1 -s 0.1 -s 0.1 -s 0.8
xfconf-query -c xfce4-panel -p /panels/panel-1/size -s 28
xfconf-query -c xfce4-panel -p /panels/panel-1/length -s 100
xfconf-query -c xfce4-panel -p /panels/panel-1/position -s "p=8;x=0;y=0"

# Desktop settings - clean and minimal
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorVNC-0/workspace0/last-image -s ""
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorVNC-0/workspace0/color-style -s 0
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorVNC-0/workspace0/rgba1 -s -a -t double -s 0.1 -s 0.1 -s 0.1 -s 1.0

# Window Manager settings - minimal decorations
xfconf-query -c xfwm4 -p /general/borderless_maximize -s true
xfconf-query -c xfwm4 -p /general/cycle_hidden -s false
xfconf-query -c xfwm4 -p /general/cycle_minimum -s false
xfconf-query -c xfwm4 -p /general/workspace_count -s 1

# Remove desktop icons and unnecessary elements
xfconf-query -c xfce4-desktop -p /desktop-icons/style -s 0

echo "XFCE minimal configuration applied successfully"