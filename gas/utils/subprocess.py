#!/usr/bin/env python

import sys
import shlex
import subprocess
from subprocess import PIPE, STDOUT #Necessary module loading: pip3 install subprocess32

def run(cmd, env=None, cwd=None, errors=None, out=PIPE):
    result = subprocess.run(shlex.split(cmd), stdout=out, stderr=errors, encoding=sys.stdout.encoding, env=env, cwd=cwd)
    return result.stdout.rstrip()

def call(cmd, env=None, cwd=None, errors=None, out=PIPE):
    subprocess.call(shlex.split(cmd), stdout=out, stderr=errors, encoding=sys.stdout.encoding, env=env, cwd=cwd)

def popenCommunicate(cmd, inData):
    process = subprocess.Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, encoding=sys.stdout.encoding)
    return process.communicate(input=inData)[0].rstrip()