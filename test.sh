#!/bin/bash
if [[ "$(SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 03-02)" != "$(SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 03-02)" ]];  then echo "Randomized topics passed";else  exit 1;fi
if [[ "$(SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 05-02)" != "$(SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 05-02)" ]];  then echo "Randomized quotes passed";else  exit 2;fi
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 02-01 | grep "Uist" | wc -l >/dev/null && echo "Static quote passed" || exit $?
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 05-01 | grep Beltane | wc -l >/dev/null && echo "Static topic passed" || exit $?
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode holiday --date 04-30 | grep "May Day" | wc -l >/dev/null && echo "Holiday test passed" || exit $?
