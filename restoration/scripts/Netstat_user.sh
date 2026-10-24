#!/bin/sh
#ScriptName=Netstate
#description=Show Active Internet connections and Active UNIX domain sockets 
netstat | grep tcp
netstat | grep unix
exit 0