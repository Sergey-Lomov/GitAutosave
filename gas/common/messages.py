#!/usr/bin/env python

notInitMessage = "Looks like gas was not initialized at this repo. Use 'gas init' to initialize."
invalidFlagFormat = "Undefined flag {} will be ignored"
noSavesAvailable = "No saves available"
nothingToSave = "Nothing to save"
saveSelectionMessage = "Please, enter index of save to restoring. Enter anything else to cancel.\n"
noAutosavesRunnedMessage = "No autosaves runned for now"
autosaveSelectionMessage = "Please, enter index of process if you want to stop autosaving. In other case press enter.\n"
workstationIdSettedFormat = "Workstation id is: {}. Please don't change it."
workstationTitleInputMessage = "Please, specify workstation title\n"
workstationTitleSettedFormat = "Current workstation title is {}. You may change it by '{}' at git config."
remoteInputMessage = "Please, specify name of remote, which should be used for autosaving. Skip for use origin.\n"
remoteSettedFormat = "Current remote is {}. You may change it by '{}' at git config."
clearApproveMessage = "All saved states will be removed. Are you sure? (y/n) "
savePeriodUndefinedFormat = "Autosaving unavailable because autosave period is undefined. You may specify autosave period by '{}' config key and restart autosaving uses '{}' command."
runAutosaveWithoutPeriodMessage = "Autosave script was called with no period"
autosaveProcessMissedMessage = "Autosave process not runned at this repo. Use 'gas autosave' to show all runned autosave processes." #TODO: validate recomended command
autosaveTerminationFormat = "Stop autosave at dir: {}"