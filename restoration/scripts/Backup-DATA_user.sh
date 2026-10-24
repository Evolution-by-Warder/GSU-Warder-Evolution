#!/bin/sh
#ScriptName=Backup dir DATA
#description=Backup dir /data to /media/hdd/data-backup.tar
rm -rf /media/hdd/data-backup.tar
tar -cf /media/hdd/data-backup.tar /data
exit 0
