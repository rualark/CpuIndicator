import os
import re
from collections import deque
from gi import require_version
from gi.repository import Gtk
from gi.repository.GLib import timeout_add, source_remove, idle_add, unix_signal_add, PRIORITY_HIGH
require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appIndicator

from cpulib.run import run, run_nowait
from cpulib.config import config


def get_cpu_jiffies():
    result = run("grep 'cpu ' /proc/stat", shell=True)
    splitted = re.split(' +', result)
    assert splitted[0] == 'cpu'
    return list(map(int, splitted[1:5]))


def get_cpu_usage(hist):
    first = hist[0]
    second = hist[-1]
    used = second[0] + second[1] + second[2] - first[0] - first[1] - first[2]
    total = used + second[3] - first[3]
    if not total:
        return 0
    return 100 * used / total


class TaskBarIcon():
    def __init__(self):
        self.cur_icon = ''
        self.ind = appIndicator.Indicator.new(
            "CpuIndicator",
            os.path.abspath("img/unknown.png"),
            appIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appIndicator.IndicatorStatus.ACTIVE)
        self.create_menu()
        self.ind.set_menu(self.menu)

        self.hist = deque()

        timeout_add(config['GUI_MS_BETWEEN_REDRAWS'], self.update)

    def update(self):
        self.update_icon()
        return True

    def update_icon(self):
        self.hist.append(get_cpu_jiffies())
        if len(self.hist) > config['SMOOTH_CYCLES']:
            self.hist.popleft()
        percent = get_cpu_usage(self.hist)
        if percent < 10:
            rounded = int(percent) + 1
        else:
            rounded = int((percent // 10 + 1) * 10)
        if rounded > 100:
            rounded = 100

        self.set_icon(rounded)


    def set_icon(self, percent):
        full_path = 'img/red-percent-' + str(percent) + '.png'
        if self.cur_icon == full_path:
            return
        self.cur_icon = os.path.abspath(full_path)

        self.ind.set_icon_full(self.cur_icon, '')

    def create_menu(self):
        self.menu = Gtk.Menu()

        self.menu.monitor = Gtk.MenuItem(label='Open System monitor')
        self.menu.monitor.connect("activate", self.on_monitor)
        self.menu.append(self.menu.monitor)

        self.menu.append(Gtk.SeparatorMenuItem.new())

        self.menu.exit = Gtk.MenuItem(label='Exit CPU indicator')
        self.menu.exit.connect("activate", self.on_exit)
        self.menu.append(self.menu.exit)

        self.menu.show_all()

    def on_monitor(self, widget):
        run_nowait('gnome-system-monitor', shell=True)

    def on_exit(self, widget):
        self.exit()

    def exit(self):
        Gtk.main_quit()


