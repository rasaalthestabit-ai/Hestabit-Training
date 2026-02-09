#!/bin/bash
URL="http://localhost:3000/"
while true; do
    STATUS=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" $URL)
    exitCode=$?
    if [ ${exitCode} -ne 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - FAILURE: Server not reachable. Exit Code: $exitCode" >> "./logs/health.log"
    fi
 
    sleep 10
done

