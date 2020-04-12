import json
from tabulate import tabulate

from gas.common.constants import *
from gas.common.messages import invalidFlagFormat
from gas.common.enumerations import Flags
from gas.utils.execution import run, call

def mainDir():
    return run('git rev-parse --show-toplevel') + "/" #TODO: Change to path separator related to os or remove

def lastListElement(list):
    legth = len(test_list)
    if legth > 0:
        return list[legth - 1]

def nomalisedUsername():
    return getFromConfig("user.name").replace(" ", ".")

def setToConfig(setting, value, isGlobal=False):
    globalComponent = " --global" if isGlobal else ""
    call("git config " + setting + " " + value + globalComponent)

def getFromConfig(setting):
    return run("git config " + setting)  
   
def metaListRow(metaDict, index):
    status = "Current: " if metaDict[metaWorkstationIdKey] == getFromConfig(configWorkstationId) else ""
    return [index, status, metaDict[metaWorkstationTitleKey], metaDict[metaTimeKey], metaDict[metaStateKey]]

def metaDict(sha):
    metaJson = run("git cat-file -p " + sha)
    return json.loads(metaJson)
      
def printMetasDicts(metasDicts):
    def createRow(metaDict): return metaListRow(metaDict, metasDicts.index(metaDict))
    rows = list(map(createRow, metasDicts))
    print(tabulate(rows, headers=savesListHeaders))

def flagForString(string): 
    for name, flag in Flags.__members__.items():
        if string in flag.value:
            return flag
                
def flagsForStrings(strings, quite=False): 
    flags = []
    for string in strings:
        flag = flagForString(string)
        if flag:
            flags.append(flag)
        elif not quite:
            print(invalidFlagFormat.format(string))
    return flags