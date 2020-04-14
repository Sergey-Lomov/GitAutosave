#!/usr/bin/env python

import sys
import platform
import wmi  # pip install WMI, pip install pywin32

from gas.utils.execution import run
from gas.common.constants import autosaveScriptFile, unknownAutosaveDir

class AutosaveProcess:
    def __init__(self, pid, directory):
        self.pid = pid
        self.directory = directory

def __processesWin():
    _wmi = wmi.WMI()
    wql = "SELECT CommandLine, ProcessId FROM Win32_Process WHERE commandline LIKE '%" + autosaveScriptFile + "%'"
    processes = list()
    for process in _wmi.query(wql):
        pid = process.ProcessId
        directory = unknownAutosaveDir
        commandComponents = process.CommandLine.split("~") 
        if len(commandComponents) >= 1:
            directory = commandComponents[-1]
        processes.append(AutosaveProcess(pid, directory))
    return processes

def allProcesses():
    if platform.system() == "Windows":
        return __processesWin()
    else:
        #Only MAC OS is currently supported, but lets try
        return "Mac OS"

def processForDir(dir):
    return next( filter(lambda item: dir == item.directory, allProcesses()), None)

def terminateProcess(process):
    _wmi = wmi.WMI()
    for process in _wmi.Win32_Process (ProcessId=process.pid):
        process.Terminate()
    
    