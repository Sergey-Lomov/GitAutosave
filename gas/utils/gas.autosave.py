#!/usr/bin/env python

import sys
import time
#from subprocess import DEVNULL

from gas.common import messages
from gas.common.enumerations import Flags
from gas.utils.execution import call
from gas.utils.services import flagsForStrings

def main():

    if len(sys.argv) < 2:
        print(messages.runAutosaveWithoutPeriodMessage)
        return

    period = int(sys.argv[1])
    flagsArgs = sys.argv[2:]
    flags = flagsForStrings(flagsArgs, quite=True)
    forced = Flags.forced in flags
    saveCmd = "gas save --forced" if forced else "gas save"
    
    while True:
        call(saveCmd, hideCLI=True)
        time.sleep(period)

main()        