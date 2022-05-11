#!/bin/bash

# Example usage:
# ./log-query.sh mm6 img thepath exec p1 'p"2' "p'3"

paso_api_log='http://paso.tol.sanger.ac.uk/log'


json_escape () {
	echo "${1//\"/\\\"}"
}

log_usage () {
	local user=$(json_escape "${1}") ; shift
	local image=$(json_escape "${1}") ; shift
	local path=$(json_escape "${1}") ; shift
	local executable=$(json_escape "${1}") ; shift

	# Escape and quote parameters, if any
	local parameters=""
	for p in $@
	do
		parameters=$(printf "${parameters} %s" $p)
	done
	parameters=$(json_escape "${parameters}")

	# Escape into JSON
	local post_data=$( printf '{"user":"%s","image":"%s","executable":"%s","path":"%s","parameters":"%s"}' "${user}" "${image}" "${executable}" "${path}" "${parameters}" )

	# POST to logging API
	curl --silent \
	-H "Accept: application/json" \
	-H "Content-Type:application/json" \
	-X POST \
	--data "${post_data}" \
	"${paso_api_log}"
}

if [[ $# < 4 ]]
then
	echo "USAGE: log.sh USER_NAME IMAGE_NAME PATH_NAME EXECUTABLE_NAME [PARAMETER PARAMETER ...]"
else
	log_usage $@
fi
