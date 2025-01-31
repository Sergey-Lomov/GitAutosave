#!/usr/bin/env python

from enum import Enum

class Flags(Enum):
    quiet = ["--quiet", "-q"]
    forced = ["--forced", "-f"]
    all = ["--all", "-a"]
    noCurrent = ["--no-current", "-nc"]
    noPreRestore = ["--no-pre-restore", "-npr"]
    start = ["--start", "-S"]
    stop = ["--stop"]

class Subcommands(Enum):
    list = "list"
    save = "save"
    restore = "restore"
    help = "help"
    init = "init"
    clean = "clean"
    autosave = "autosave"
    version = "version"