# FireStick C2 Server

### Install Some Crontab that calls /update/all every 5 minutes or so
*/5 * * * * curl http://localhost:9371/update/all >/dev/null 2>&1