#!/bin/sh
#ScriptName=Restore SD card
#description=Restore SD card /media/cf from /media/hdd/cf-backup.tar
tar xvf /media/hdd/cf-backup.tar -C / 
exit 0
