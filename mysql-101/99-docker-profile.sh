DOCKER=$(which docker)
dip(){
# Show docker ips
        local arg=${1}
        if [ -z "$arg" ]; then
                arg=$(docker ps -q)
        fi
        $DOCKER inspect --format ' {{.Name}} {{.NetworkSettings.IPAddress}}' $arg
}


#
# Docker Exec alias with auto-complete
#
dshell(){
        local container="${1##/}"
        local command="${2:-/bin/bash}"
        $DOCKER exec -ti "$container" "$command"
}
_dshell()
{
  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts="$(docker inspect -f '{{.Name}}' $(docker ps -q))"
  opts=${opts//\/}

  if [[ ${cur} =~ [a-z]+ ]]; then
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
      return 0
  fi
}
complete -F _dshell dshell

