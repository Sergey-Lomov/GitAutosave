#!/usr/bin/env python

gasIndex = "gas_index"
refsDir = "refs/gas/"
metaBlobPrefix = "meta."
stateTreePrefix = "state."
preRestoreTitle = "Pre-restore"
preRestoreId = "pre-restore-id"
savesListHeaders = ["#", "", "Workstation", "Save time", "State tree SHA"]
dateFormat = "%Y-%m-%d %H:%M:%S"

#TODO: Implement configs and meta keys as enums
configWorkstationId = "gas.workstation.id"
configWorkstationTitle = "gas.workstation.title"
configRemote = "gas.remote"

metaTimeKey = "time"
metaWorkstationIdKey = "workstationId"
metaWorkstationTitleKey = "workstationTitle"
metaStateKey = "state"