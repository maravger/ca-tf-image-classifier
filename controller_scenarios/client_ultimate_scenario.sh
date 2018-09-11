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
end=100
# Execute script
echo "Phase 1 of 5: App0 2->18->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 18 $end
echo "Phase 1 of 5 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

# App1: 2->21->2
end=110
# Execute script
echo "Phase 2 of 5: App1 2->21->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app1.py 2 21 $end
echo "Phase 2 of 5 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

# App0: 2->36->2
end=200
# Execute script
echo "Phase 3 of 5: App0 2->36->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 36 $end
echo "Phase 3 of 5 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

# App1: 2->43->2
end=220
# Execute script
echo "Phase 4 of 5: App0 2->43->2, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app1.py 2 43 $end
echo "Phase 4 of 5 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo

# App0: 2->36->2 & 43->2->43
end=220
# Execute script
echo "Phase 5 of 5: App0 2->36->2 & 43->2->43, for ${end}min. Initiated at: $(date '+%d/%m/%Y %H:%M:%S')"  
python3.5 client_app0.py 2 36 $end &
python3.5 client_app1.py 43 43 $end 
echo "Phase 5 of 5 ended at: $(date '+%d/%m/%Y %H:%M:%S')"
echo
