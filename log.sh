#!/bin/bash

# Example usage:
# ./log.sh mm6 img thepath exec p1 'p"2' "p'3"

paso_api_log='http://127.0.0.1:5000/log'

json_escape () {
	echo "${1//\"/\\\"}"
    #printf '%s' "$1" | python -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
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
	#post_data=$(printf "%q" "${post_data}" )
	echo ${post_data}

	# POST to logging API
	curl -i \
	-H "Accept: application/json" \
	-H "Content-Type:application/json" \
	-X POST \
	--data "${post_data}" \
	"${paso_api_log}"
}

log_usage $@
