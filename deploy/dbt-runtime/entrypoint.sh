#!/bin/sh
cd src && dbt init dbt_demo
su app
trap : TERM INT
tail -f /dev/null & wait
