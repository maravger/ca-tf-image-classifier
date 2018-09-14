#!/usr/bin/env bash

# Set interval (duration) in seconds.
#min=60

# Trap ctrl-c (INT) and call cleanup()
trap cleanup INT

function cleanup() {
    echo
	echo "** Terminating Client Ultimate Script and cleaning up..."
	
	# Stop redis server
	echo "Step 1/2: Killing client of app0..."
	pkill -9 -f client_app0.py

	# Kill celery worker
	echo "Step 2/2: Killing client of app1..."
	pkill -9 -f client_app1.py
}

# App0: 2->18->2
end=86
# Execute script
echo "Phase 1 of 7: App0 2->18->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 18 $end
echo "Phase 1 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App1: 2->21->2
end=96
# Execute script
echo "Phase 2 of 7: App1 2->21->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app1.py 2 21 $end
echo "Phase 2 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App0: 2->36->2
end=180
# Execute script
echo "Phase 3 of 7: App0 2->36->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 36 $end
echo "Phase 3 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App1: 2->43->2
end=210
# Execute script
echo "Phase 4 of 7: App0 2->43->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app1.py 2 43 $end
echo "Phase 4 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App0: 2->36->2 & 43->2->43
end=210
# Execute script
echo "Phase 5 of 7: App0 2->36->2 & 43->2->43, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 36 $end &
python3.5 client_app1.py 43 43 $end 
echo "Phase 5 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App0: 2->36->2 &-2->43->2
end=210
# Execute script
echo "Phase 6 of 7: App0 2->36->2 & 2->43->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 36 $end &
python3.5 client_app1.py 2 43 $end 
echo "Phase 6 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

sleep 10m

# App0: 36->2->18 & 21->43->2
end=210
# Execute script
echo "Phase 7 of 7: App0 36->2->18 & 21->43->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 36 36 $end &
python3.5 client_app1.py 20 43 $end 
echo "Phase 7 of 7 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo
