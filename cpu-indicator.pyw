#!/usr/bin/env python
# coding=utf-8
# This script uses python3

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk

from cpulib.icon import TaskBarIcon

def main():
    TaskBarIcon()

    Gtk.main()


if __name__ == '__main__':
    main()
