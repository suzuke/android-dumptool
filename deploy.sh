#!/bin/sh

# Build
ndk-build

# Push
adb push libs/armeabi/dumptool /data/local/tmp
adb push libs/armeabi/dumpmem /data/local/tmp

