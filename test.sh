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
test="AM topic test"
echo "Running ${test}"
[[ "`SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 03-02 --pod 1| grep 'Fir Bolg'| wc -l`" == "1" ]] && true || false
passfail "${test}" $?
test="PM topic test"
echo "Running ${test}"
[[ "`SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode topic --date 03-02 --pod 2| grep 'celtic' | wc -l`" == "0" ]] && true || false
passfail "${test}" $?
# test="AM quote test"
# echo "Running ${test}"
# [[ "`SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 02-13 --pod 1| grep 'Nest at Bride' | wc -l`" == "1" ]] && true || false
# passfail "${test}" $?
# test="PM quote test"
# echo "Running ${test}"
# [[ "`SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 02-13 --pod 2| grep 'Three fair lords' | wc -l`" == "1" ]] && true || false
# passfail "${test}" $?
# test="PM quote undated test"
# echo "Running ${test}"
# [[ "`SERVER= ACCESS_TOKEN= python3 src/celtibot.py --dryrun 1 --mode quote --date 01-08 --pod 2| grep 'Better snow than no rain-storm' | wc -l`" != "1" ]] && true || false
# passfail "${test}" $?
