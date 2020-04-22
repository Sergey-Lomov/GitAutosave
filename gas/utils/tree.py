#!/usr/bin/env python

import datetime
import json
import os
from subprocess import DEVNULL

from gas.common.constants import *
from gas.utils.services import getFromConfig, nomalisedUsername, metaDict
from gas.utils.execution import run, call, popenCommunicate

def workstationsListRef():
    return refsDir + nomalisedUsername()
    
def workstationRef(workstation):
    return refsDir + nomalisedUsername() + workstationRefSeparator + workstation
    
def currentWorkstationRef():
    currentId = getFromConfig(configWorkstationId)
    return workstationRef(currentId)
    
def workstationsRefs():
    workstations = run("git cat-file -p " + workstationsListRef())
    refs = list()
    for workstation in workstations.splitlines():
        refs.append(workstationRef(workstation))
    return refs

def workstationsBlob():
    return run("git rev-parse " +  workstationsListRef())
    
def checkWorkstationsListRef():
    listRef = run("git rev-parse --verify --quiet " + workstationsListRef())
    return True if listRef else False

def itemSha(item):
    shaAndName = item.split(" ")[2]
    return shaAndName.split("\t")[0]

def blobItem(sha, title):
    return "100644 blob " + sha + "\t" + title
    
def treeItem(sha, title):
    return "040000 tree " + sha + "\t" + title
    
def treeItems(sha):
    listing = run("git ls-tree " + sha).splitlines()
    iterator = map(str.rstrip, listing)
    return list(iterator)

def createTree(items):
    data = os.linesep.join(items)
    return popenCommunicate("git mktree", data)

def createMetaBlob(state, customTitle=None, customId=None):
    workstationId = customId if customId else getFromConfig(configWorkstationId)
    workstationTitle = customTitle if customTitle else getFromConfig(configWorkstationTitle)
    now = datetime.datetime.now()
    meta = {
        metaWorkstationIdKey: workstationId,
        metaWorkstationTitleKey: workstationTitle,
        metaTimeKey: now.strftime(dateFormat),
        metaStateKey: state
    }
    metaJson = json.dumps(meta)
    return popenCommunicate("git hash-object -w --stdin", metaJson)

def createStateTree():
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = ".git/" + gasIndex
    call("git add .", env)
    return run("git write-tree", env=env)

def updateMetaInItems(items, metaBlobSha):
    newItems = list(filter(lambda item: not metaBlobName in item, items))
    newItems.append(blobItem(metaBlobSha, metaBlobName))
    return newItems

def updateStateInItems(items, stateTreeSha):
    newItems = list(filter(lambda item: not stateTreeName in item, items))
    newItems.append(treeItem(stateTreeSha, stateTreeName))
    return newItems

def getStateFromItems(items):
    filtered = list(filter(lambda item: stateTreeName in item, items))
    item = next(iter(filtered), None)
    if item:
        return itemSha(str(item))

def fetchRef(ref, hideErrors=False):
    remote = getFromConfig(configRemote)
    errors = DEVNULL if hideErrors else None
    cmd = "git fetch --quiet -f " + remote + " " + ref + ":" + ref
    print(cmd)
    call(cmd, errors=errors, out=errors)

def fetchListRef(hideErrors=False):
    ref = workstationsListRef()
    fetchRef(ref, hideErrors)
    
def fetchAllRefs(hideErrors=False):
    fetchListRef(hideErrors)
    for ref in workstationsRefs():
        fetchRef(ref, hideErrors=True)  #ref may be unavailable, if no save available from specified workstation

def updateRef(ref, sha, quiet=False, renewRemote=True):
    quietComponent = " --quiet" if quiet else ""
    call("git update-ref " + ref + " " + sha)
    if renewRemote:
        call("git push --force " + getFromConfig(configRemote) + " " + ref + quietComponent)

def saveCurrentState(state=None, quiet=False, customTitle=None, customId=None):
    workstation = customId if customId else getFromConfig(configWorkstationId)
    currentState = state if state else createStateTree()
    registerWorkstation(workstation)
    
    ref = workstationRef(workstation)
    if ref:
        items = treeItems(ref)
    else:
        items = list()
    
    meta = createMetaBlob(currentState, customTitle=customTitle, customId=customId)
    items = updateMetaInItems(items, meta)
    items = updateStateInItems(items, currentState)
    workstationTree = createTree(items)
    updateRef(ref, workstationTree, quiet=quiet)
    
def availableMetas(withFetch=False, noCurrent=False):
    if withFetch:
        fetchAllRefs()
        
    refs = workstationsRefs()
    currentId = getFromConfig(configWorkstationId)
    metaDicts = list()
   
    for ref in refs:
        if noCurrent and currentId in ref:
            continue
        items = treeItems(ref)
        stationMetaItems = filter(lambda item: metaBlobName in item, items)
        stationMetaShas = map(itemSha, stationMetaItems)
        stationMetaDicts = map(metaDict, stationMetaShas)
        metaDicts.extend(stationMetaDicts)

    return metaDicts
    
def registerWorkstation(uuid):
    fetchListRef(hideErrors=True)
    
    if not checkWorkstationsListRef():
        workstations = uuid
    else:
        workstations = run("git cat-file -p " + workstationsListRef())
        if uuid in workstations:
            return
        workstations = workstations + "\n" + uuid
            
    listSha = popenCommunicate("git hash-object -w --stdin", workstations)
    updateRef(workstationsListRef(), listSha, quiet=True)
    
