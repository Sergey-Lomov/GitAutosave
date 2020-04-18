#!/usr/bin/env python

version = "0.1.0"

gasIndex = "gas_index"
refsDir = "refs/gas/"
metaBlobPrefix = "meta."
stateTreePrefix = "state."
preRestoreTitle = "Pre-restore"
preRestoreId = "pre-restore-id"
savesListHeaders = ["#", "", "Workstation", "Save time", "State tree SHA"]
autosaveProcessesHeaders = ["#", "Directory"]
dateFormat = "%Y-%m-%d %H:%M:%S"
autosaveScriptFile = "gas.autosave.py"
autosaveLogFile = "autosave.log"
unknownAutosaveDir = "unknown"
autosaveDirSeparator = "?"

#TODO: Implement configs and meta keys as enums
configWorkstationId = "gas.workstation.id"
configWorkstationTitle = "gas.workstation.title"
configRemote = "gas.remote"
configSavePeriod = "gas.save.period"

metaTimeKey = "time"
metaWorkstationIdKey = "workstationId"
metaWorkstationTitleKey = "workstationTitle"
metaStateKey = "state"