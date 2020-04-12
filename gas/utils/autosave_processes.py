#!/usr/bin/env python

import sys
import time
import platform

class AutosaveProcess:
    def __init__(self, pid, directory):
        self.pid = pid
        self.directory = directory

def autosaveProcess(dir):
    if platform.system() == "Windows":
        return "Windows"
    else:
        #Only MAC OS is currently supported, but lets try
        return "Mac OS"
      