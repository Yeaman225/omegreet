import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import platform
import psutil
import os
import sys
from datetime import datetime

class WelcomeScreen(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to Linux")
        self.set_default_size(800, 600)
        self.set_border_width(20)

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # Welcome message
        distro = "OMEGA UI -1" # Changed distro name
        welcome_label = Gtk.Label()
        welcome_label.set_markup(f'<span font="Poppins 16" weight="bold">Welcome to {distro}</span>')
        main_box.pack_start(welcome_label, False, False, 20)

        # System Information Frame
        info_frame = Gtk.Frame(label="System Information")
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_frame.add(info_box)
        info_frame.set_margin_bottom(10)

        # System info details
        self.add_info_row(info_box, "OS", platform.system())
        self.add_info_row(info_box, "Kernel Version", platform.release())
        self.add_info_row(info_box, "Architecture", platform.machine())
        self.add_info_row(info_box, "CPU", platform.processor())
        self.add_info_row(info_box, "RAM", f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB")
        self.add_info_row(info_box, "Hostname", platform.node())

        main_box.pack_start(info_frame, False, False, 0)

        # Usage Statistics Frame
        usage_frame = Gtk.Frame(label="Current Usage")
        usage_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        usage_frame.add(usage_box)
        usage_frame.set_margin_bottom(10)

        # Usage details
        self.usage_labels = {}
        self.update_usage_stats(usage_box)

        main_box.pack_start(usage_frame, False, False, 0)

        # Controls
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.set_halign(Gtk.Align.CENTER)

        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", self.on_refresh_clicked)
        controls_box.pack_start(refresh_btn, False, False, 0)

        main_box.pack_start(controls_box, False, False, 20)

        # Keyboard shortcuts
        hints_label = Gtk.Label(label="Press 'Q' to quit | Press 'R' to refresh")
        hints_label.set_margin_top(10)
        main_box.pack_start(hints_label, False, False, 0)

        # Key bindings
        self.connect("key-press-event", self.on_key_press)

    def add_info_row(self, parent, label, value):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_widget = Gtk.Label(label=f"{label}:")
        label_widget.set_width_chars(15)
        label_widget.set_xalign(0)
        value_widget = Gtk.Label(label=value)
        value_widget.set_xalign(0)

        box.pack_start(label_widget, False, False, 0)
        box.pack_start(value_widget, False, False, 0)
        parent.pack_start(box, False, False, 5)

        return value_widget

    def update_usage_stats(self, parent=None):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        if not self.usage_labels:
            self.usage_labels["CPU"] = self.add_info_row(parent, "CPU Usage", f"{cpu_usage}%")
            self.usage_labels["RAM"] = self.add_info_row(parent, "RAM Usage", f"{ram_usage}%")
            self.usage_labels["Disk"] = self.add_info_row(parent, "Disk Usage", f"{disk_usage}%")
        else:
            self.usage_labels["CPU"].set_text(f"{cpu_usage}%")
            self.usage_labels["RAM"].set_text(f"{ram_usage}%")
            self.usage_labels["Disk"].set_text(f"{disk_usage}%")

        return True

    def on_refresh_clicked(self, button):
        self.update_usage_stats()

    def on_key_press(self, widget, event):
        keyval = event.keyval
        keyval_name = Gdk.keyval_name(keyval)

        if keyval_name.lower() == 'q':
            Gtk.main_quit()
        elif keyval_name.lower() == 'r':
            self.update_usage_stats()

        return True

def text_based_welcome():
    """Display system information in text mode for Replit environment"""
    distro = "OMEGA LINUX -1"

    print(f"\n{'='*60}")
    print(f"Welcome to {distro}".center(60))


def main():
    try:
        app = WelcomeScreen()
        app.connect("destroy", Gtk.main_quit)
        app.show_all()
        # Update usage stats every 5 seconds
        GLib.timeout_add_seconds(5, app.update_usage_stats)
        Gtk.main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
