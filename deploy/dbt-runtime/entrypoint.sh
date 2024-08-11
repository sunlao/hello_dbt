#!/bin/sh
cd src && dbt init hello && dbt parse
su app
trap : TERM INT
tail -f /dev/null & wait
