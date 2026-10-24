#!/bin/sh
#ScriptName=Backup SD card
#description=Backup SD card /media/cf to /media/hdd/cf-backup.tar
rm -rf /media/hdd/cf-backup.tar
tar -cf /media/hdd/cf-backup.tar /media/cf
exit 0
