# FireStick C2 Server

### Install Some Crontab that calls /update/all every 5 minutes or so
```
*/5 * * * * curl http://localhost:9371/update/all >/dev/null 2>&1
```

### Also need adb etc state checks. Every 5 seconds ?????
```
while true ; do curl http://localhost:9371/state/check & sleep 5; done
```

### Refresh Twitch OAuth Code , Valid for 60 Days

https://dev.twitch.tv/docs/authentication/getting-tokens-oauth

```
curl -X POST 'https://id.twitch.tv/oauth2/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'client_id=<your client id goes here>&client_secret=<your client secret goes here>&grant_type=client_credentials'
```