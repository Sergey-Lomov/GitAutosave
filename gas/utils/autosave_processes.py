#!/usr/bin/env python

import sys
import platform
import wmi  # pip install WMI, pip install pywin32

from gas.utils.execution import run
from gas.common.messages import *
from gas.common.constants import autosaveScriptFile

class AutosaveProcess:
    def __init__(self, pid, directory):
        self.pid = pid
        self.directory = directory

def __processesWin():
    _wmi = wmi.WMI()
    wql = "SELECT CommandLine, ProcessId FROM Win32_Process WHERE commandline LIKE '%" + autosaveScriptFile "%'"
    return _wmi.query(wql).first

def processForDir(dir):
    if platform.system() == "Windows":
        process = __processForDirWin(dir)
    else:
        #Only MAC OS is currently supported, but lets try
        return "Mac OS"
      
    if not process:
        print(autosaveProcessMissedMessage)
    