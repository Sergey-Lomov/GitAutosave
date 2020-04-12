#!/usr/bin/env python

import sys
import os
import platform
import shlex
import subprocess
from subprocess import PIPE, STDOUT, DEVNULL #Necessary module loading: pip3 install subprocess32

def run(cmd, env=None, cwd=None, errors=None, out=PIPE):
    result = subprocess.run(shlex.split(cmd), stdout=out, stderr=errors, encoding=sys.stdout.encoding, env=env, cwd=cwd)
    return result.stdout.rstrip()

def call(cmd, env=None, cwd=None, errors=None, out=PIPE, hideCLI=False):
    startupinfo = subprocess.STARTUPINFO()
    if hideCLI:
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(shlex.split(cmd), stdout=out, stderr=errors, encoding=sys.stdout.encoding, env=env, cwd=cwd, startupinfo=startupinfo)

def popenCommunicate(cmd, inData, cwd=None):
    process = subprocess.Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, encoding=sys.stdout.encoding, cwd=cwd)
    return process.communicate(input=inData)[0].rstrip()
    
def backgroundDetachedPopen(cmd, cwd=None, logfile=None):
    kwargs = {}
    if platform.system() == 'Windows':
        # from msdn [1]
        CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
        DETACHED_PROCESS = 0x00000008          # 0x8 | 0x200 == 0x208
        kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)  
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs.update(startupinfo=startupinfo)  
    elif sys.version_info < (3, 2):  # assume posix
        kwargs.update(preexec_fn=os.setsid)
    else:  # Python 3.2+ and Unix
        kwargs.update(start_new_session=True)
    p = subprocess.Popen(shlex.split(cmd), 
                            encoding=sys.stdout.encoding, 
                            cwd=cwd, 
                            close_fds=True,
                            stdout=logfile, stderr=logfile,
                            **kwargs)
    assert not p.poll()
    return p