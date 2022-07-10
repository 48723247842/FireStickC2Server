#!/bin/bash
function is_int() { return $(test "$@" -eq "$@" > /dev/null 2>&1); }

# reset git on new vps box ???
# ssh-add -D || sudo pkill -9 ssh-agent && eval `ssh-agent -s` && ssh-add -D
# ssh-add -k /home/morphs/.ssh/48723247842_Github
# ssh -vT git@github.com
# then you can proceed as normal ?

ssh-add -D || sudo pkill -9 ssh-agent && eval `ssh-agent -s` && ssh-add -D
git init
git remote remove origin
git config --global --unset user.name
git config --global --unset user.email
git config user.name "48723247842"
git config user.email "48723247842@protonmail.com"
# ssh-add -k /Users/morpheous/Tresors/Misc/SSH2/KEYS/48723247842_Github
ssh-add -k /home/morphs/.ssh/48723247842_Github

LastCommit=$(git log -1 --pretty="%B" | xargs)
# https://stackoverflow.com/a/3626205
if $(is_int "${LastCommit}");
    then
    NextCommitNumber=$((LastCommit+1))
else
   echo "Not an integer Resetting"
   NextCommitNumber=1
fi
git add .
git commit -m "$NextCommitNumber"
git remote add origin git@github.com:48723247842/FireStickC2Server.git
git push origin master