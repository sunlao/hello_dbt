#!/bin/sh
su app
trap : TERM INT
tail -f /dev/null & wait
