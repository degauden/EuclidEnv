#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    confscr=`/usr/bin/which Euclid_config.sh`
    . ${confscr} "$@" > /dev/null 2>&1
    unset confscr
  fi

  elogscr=`/usr/bin/which Elogin.sh`
  if [[ -e ${elogscr} ]]; then
    if [[ -n "$ELOGIN_DONE" ]]; then
      # The login part has already been done. Only the shell (setup) part is redone.
      # This is mandatory for the creation of a subshell.
      . ${elogscr} --shell-only --silent "$@" > /dev/null 2>&1
    else
      # The full login and setup is not performed.
      export E_BANNER=`mktemp`
      . ${elogscr} --quiet "$@" >> ${E_BANNER}
      
      if [[ ! -n "$EUCLID_POST_DONE" ]]; then
        if [[ -n "$EUCLID_POST_SCRIPT" ]]; then
          epostscr=`/usr/bin/which $EUCLID_POST_SCRIPT.sh`
          if [[ -r ${epostscr} ]]; then
            . ${epostscr} "$@" >> ${E_BANNER}
            export EUCLID_POST_DONE=yes
          fi
          unset epostscr
        fi
      fi
            
      
    fi
  fi
  unset elogscr

fi

