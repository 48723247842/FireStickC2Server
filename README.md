# FireStick C2 Server

### Install Some Crontab that calls /update/all every 5 minutes or so
```
*/5 * * * * curl http://localhost:9371/update/all >/dev/null 2>&1
```

### Also need adb etc state checks. Every 5 seconds ?????
```
while true ; do curl http://localhost:9371/state/check & sleep 5; done
```