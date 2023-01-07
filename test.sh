#!/bin/bash
function passfail {
  if [[ ! $2 -eq 0 ]]; then  
  	echo "${1} failed"
	exit $2
  fi
  echo "${1} passed"
  return 0
}
test="Topic Test"
echo "Running ${test}"
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 03-02 >/dev/null 2>&1
passfail "${test}" $?
test="Quote Test"
echo "Running ${test}"
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 01-09 >/dev/null 2>&1
passfail "${test}" $?
test="Date quot test"
echo "Running ${test}"
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 02-01 | grep "Uist" | wc -l >/dev/null
passfail "${test}" $?
test="Date topic test"
echo "Running ${test}"
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 05-01 | grep Beltane | wc -l >/dev/null
passfail "${test}" $?
test="Holiday test"
echo "Running ${test}"
SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode holiday --date 04-30 | grep "May Day" | wc -l >/dev/null
passfail "${test}" $?
