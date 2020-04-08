#!/usr/bin/env python

import datetime
import json
import os
from subprocess import DEVNULL

from gas.common.constants import *
from gas.utils.services import getFromConfig, nomalisedUsername, metaDict
from gas.utils.subprocess import run, call, popenCommunicate

def userTreeRef():
    return refsDir + nomalisedUsername()

def userTree():
    return run("git rev-parse " +  userTreeRef())
    
def checkUserTree():
    userTree = run("git rev-parse --verify --quiet " + userTreeRef())
    return True if userTree else False

def metaBlobName(customId=None):
    workstationId = customId if customId else getFromConfig(configWorkstationId)
    return metaBlobPrefix + workstationId

def stateTreeName(customId=None):
    workstationId = customId if customId else getFromConfig(configWorkstationId)
    return stateTreePrefix + workstationId

def itemSha(item):
    shaAndName = item.split(" ")[2]
    return shaAndName.split("\t")[0]

def blobItem(sha, title):
    return "100644 blob " + sha + "\t" + title
    
def treeItem(sha, title):
    return "040000 tree " + sha + "\t" + title

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

def treeItems(sha):
    listing = run("git ls-tree " + sha).splitlines()
    iterator = map(str.rstrip, listing)
    return list(iterator)

def updateMetaInItems(items, metaBlobSha, customId=None):
    blobName = metaBlobName(customId)
    newItems = list(filter(lambda item: not blobName in item, items))
    newItems.append(blobItem(metaBlobSha, blobName))
    return newItems

def getStateFromItems(items):
    treeName = stateTreeName()
    filtered = list(filter(lambda item: treeName in item, items))
    item = next(iter(filtered), None)
    if item:
        return itemSha(str(item))
    else:
        return ""

def updateStateInItems(items, stateTreeSha, customId=None):
    stateTree = stateTreeName(customId)
    newItems = list(filter(lambda item: not stateTree in item, items))
    newItems.append(treeItem(stateTreeSha, stateTree))
    return newItems
    
def fetchUserRef(hideErrors=False):
    remote = getFromConfig(configRemote)
    ref = userTreeRef()
    errors = DEVNULL if hideErrors else None
    call("git fetch --quiet -f " + remote + " " + ref + ":" + ref, errors=errors)

def renewUserRef(treeSha, quiet=False, renewRemote=True):
    quietComponent = " --quiet" if quiet else ""
    call("git update-ref " + userTreeRef() + " " + treeSha)
    if renewRemote:
        call("git push --force " + getFromConfig(configRemote) + " " + userTreeRef() + quietComponent)

def saveCurrentState(quiet=False, customTitle=None, customId=None):
    items = treeItems(userTree())
    state = createStateTree()
    meta = createMetaBlob(state, customTitle=customTitle, customId=customId)
    items = updateMetaInItems(items, meta, customId=customId)
    items = updateStateInItems(items, state, customId=customId)
    newUserTree = createTree(items)
    renewUserRef(newUserTree, quiet=quiet)
    
def availableMetas(noCurrent=False):
    tree = userTree()
    items = treeItems(tree)
    blobs = filter(lambda item: metaBlobPrefix in item, items)
    if noCurrent:
        currentId = getFromConfig(configWorkstationId)
        blobs = filter(lambda item: not currentId in item, blobs)
    metasSha = list(map(itemSha, blobs))
    return list(map(metaDict, metasSha))