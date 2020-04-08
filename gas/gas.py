#!/usr/bin/env python
#Pyton 3 is necessary
import sys
import subprocess, os
import datetime
import uuid
import json
import shlex
from enum import Enum  #Necessary module loading on mac:pip3 install enum34
from subprocess import PIPE, STDOUT #Necessary module loading: pip3 install subprocess32

from gas.common import messages
from gas.common.constants import *
from gas.common.enumerations import Flags, Subcommands
from gas.utils.subprocess import run, call, popenCommunicate
from gas.utils.tree import fetchUserRef, renewUserRef, userTree, checkUserTree, createTree, createStateTree, availableMetas, saveCurrentState, treeItems, getStateFromItems
from gas.utils.services import getFromConfig, setToConfig, printMetasDicts, mainDir, flagsForStrings

#Data storing concept
"""For every user creates tree with all data, related to gas util. This tree calls 'User tree' and may be found by ref in format refs/gas/username
Users tree contains pair tree-blob for each workstation. Tree contains project state at specified workstation and calls 'State tree'
Blob contains metadata as list of key-value pairs. This lbob calls 'MetaBlob'. 
"""

def init(flags=[]):
    workstationId = getFromConfig(configWorkstationId)
    if not workstationId:
        workstationId = str(uuid.uuid1())
        setToConfig(configWorkstationId, workstationId, isGlobal=True)
    print(messages.workstationIdSettedFormat.format(workstationId))
    
    workstationTitle = getFromConfig(configWorkstationTitle)
    if not workstationTitle:
        workstationTitle = input(messages.workstationTitleInputMessage)
        setToConfig(configWorkstationTitle, workstationTitle, isGlobal=True)
    print(messages.workstationTitleSettedFormat.format(workstationTitle, configWorkstationTitle))
    
    remote = getFromConfig(configRemote)
    if not remote:
        remote = input(messages.remoteInputMessage)
        if not remote:
            remote = "origin"
        setToConfig(configRemote, remote)
    print(messages.remoteSettedFormat.format(remote, configRemote))
    
    fetchUserRef(hideErrors=True)
    if not checkUserTree():
        tree = createTree([])
        renewUserRef(tree, quiet=True)

def showHelp(flags=[]):
    print("Help stub")
    
def restore(flags=[]):
    quiet = Flags.quiet in flags
    noCurrent = Flags.noCurrent in flags
    forced = Flags.forced in flags
    noPreRestore = Flags.noPreRestore in flags

    fetchUserRef()
    
    metasDicts = availableMetas(noCurrent=noCurrent)
    if not metasDicts:
        print(messages.noSavesAvailable)
        return
    
    if len(metasDicts) > 1 or not forced:
        printMetasDicts(metasDicts)
        try:
            index = int(input(messages.saveSelectionMessage))
            if index < 0 or index >= len(metasDicts):
                return
        except:
            return
    else:
        index = 0
    
    if not noPreRestore:
        saveCurrentState(quiet=quiet, customTitle=preRestoreTitle, customId=preRestoreId)
    
    state = metasDicts[index][metaStateKey]
    cwd = mainDir().encode(sys.stdout.encoding)
    
    quietComponent = " --quiet" if quiet else ""
    call("git read-tree " + state + quietComponent, cwd=cwd)
    call("git clean -f -d" + quietComponent, cwd=cwd)
    call("git checkout ." + quietComponent, cwd=cwd)
    call("git read-tree HEAD" + quietComponent, cwd=cwd)
    
def save(flags=[]):
    forced = Flags.forced in flags
    quiet = Flags.quiet in flags

    items = treeItems(userTree())
    state = createStateTree()
    oldState = getStateFromItems(items)

    if state == oldState and not forced:
        print(messages.nothingToSave)
        return
    
    saveCurrentState(quiet=quiet)

def showList(flags=[]):
    fetchUserRef()
    metasDicts = availableMetas()
    
    if not metasDicts:
        print(messages.noSavesAvailable)
        return
        
    printMetasDicts(metasDicts)

def clean(flags=[]):
    approve = input(messages.clearApproveMessage)
    if not approve == "y":
        return
    
    clearTree = createTree([])
    renewUserRef(clearTree, quiet=True)

def start(flags=[]):
    forced = Flags.forced in flags
    autosaveCmd = "echo test1\n\
    \n echo test2"
    """while true\n\
        do\n\
            echo Test\n\
            sleep 10\n\
        done"""
    subprocess.call(shlex.split(autosaveCmd))

def main(): 
    if len(sys.argv) < 2:
        showHelp()
        return

    subcomand = sys.argv[1]
    flagsArgs = sys.argv[2:]
    flags = flagsForStrings(flagsArgs)

    if not checkUserTree() and subcomand != Subcommands.init.value:
        print(messages.notInitMessage)
        return

    switcher = {
        Subcommands.restore.value: restore,
        Subcommands.save.value: save,
        Subcommands.list.value: showList,
        Subcommands.init.value: init,
        Subcommands.clean.value: clean,
        Subcommands.start.value: start
    }
    func = switcher.get(subcomand, lambda flags: showHelp(flags))
    func(flags)