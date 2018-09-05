#!/bin/bash

# var 1 = how many clients this script will deploy
# var 2 = variable for sleeping time for python script


# kill all subshells and processes on exit
trap "kill 0" SIGINT

var1="$1"
var2="$2"
python controllerGetLogs.py &

for i in $( eval echo {1..$var1} )
do
    echo "Requests ($i) begin"
    python3.5 clientlocal_for_testing.py $var2 &
done
while true; do sleep 1000000; done
