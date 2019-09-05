#!/bin/sh
fswebcam --no-banner -r $1x$2 /root/Pics/`date +"%Y-%m-%d_%H%M%S"`.jpg
