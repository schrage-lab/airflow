#!/usr/bin/env bash

function getEnv(){
	export $(grep -v '^#' .env | xargs)
}

function airflowUp(){
	$(docker compose up -d)
}

function airflowDown(){
	$(docker compose down)
}

function airflowUi(){
	# open chrome to airflow ui
	exe="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" 
	localhost="http://localhost:8080"
	"$exe" "$localhost" </dev/null &>/dev/null &
}

function archiver(){
    local day_time_readable=$(date +'%D %T')
    echo "${day_time_readable} Beginning archive..."
    
	local timestamp=$(date +'%Y%m%d_%H%M%S')
    docker exec -u airflow airflow-postgres-1 pg_dumpall > "${LOCAL_ARCHIVE}/${timestamp}.dump" && echo "${day_time_readable} Archival successful" || echo "${day_time_readable} Archival failed"
    cp "${LOCAL_ARCHIVE}/${timestamp}.dump" "${FS_SERVER_ARCHIVE}"    
}

function getLogo(){
		logo0="  ____________       _____________"
		logo1=" ____    |__( )_________  __/__  /________      __"
		logo2="____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /"
		logo3="___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /"
		logo4=" _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/"
		logo=$(printf "\n\n%s\n%s\n%s\n%s\n%s\n\n" "$logo0" "$logo1" "$logo2" "$logo3" "$logo4" "$logo5")
		echo "$logo"
}

function main(){
    day_time_readable=$(date +'%D %T')
	
	getEnv
    
    echo "${day_time_readable} Starting Airflow..."
    airflowUp
    
	container="airflow-airflow-webserver-1"
	until [ "$( docker container inspect -f '{{.State.Status}}' $container )" == "running" ]; do
		sleep 5
	done
	
    echo "${day_time_readable} Opening Airflow UI..."
    airflowUi

	# # archive every hour
	# INTERVAL=3600

    # while true; do
		# getLogo
        # printf "\nPress '%s' to begin an archive\nPress '%s' to exit\n" 'a' 'q'
        # read -t $INTERVAL -n 1 char <&1
        
		# if [ ! -z "$char" ]; then
			# # manual archive
			# if [[ "$char" == a ]]; then
				# archiver;
			
			# elif [[ "$char" == q ]]; then
				# echo; echo "${day_time_readable} Getting final archive..."
				# archiver
				
				# echo "Shutting down Airflow..."
				# airflowDown
				
				# break
			# fi
		# else
            # archiver
        # fi
    # done
}

main