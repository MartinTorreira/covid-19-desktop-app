#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import gettext
from pathlib import Path

from controller import Controller
from model import Model
from view import View

if __name__ == '__main__':
    c = Controller(Model(), View())
    c.set_view()
    c.run()


