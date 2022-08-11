#!/bin/bash

# adb connect IP:5555

uri="vlc://https://files.34353.org/AudioBooks/HarryPotter/01-Harry-Potter-And-The-Sorcerers-Stone.mp3"
adb shell am start -a "android.intent.action.VIEW" -d "$uri"
