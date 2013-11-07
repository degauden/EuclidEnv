#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    confscr=`/usr/bin/which Euclid_config.sh`
    . ${confscr} "$@"
    unset confscr
  fi

  if [[ -n "$E_BANNER" ]]; then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unset E_BANNER
  else
    
    elogscr=`/usr/bin/which Elogin.sh`
    if [[ -e ${elogscr} ]]; then
      . ${elogscr} --quiet "$@"
    fi

    if [[ ! -n "$EUCLID_POST_DONE" ]]; then
      if [[ -n "$EUCLID_POST_SCRIPT" ]]; then
        epostscr=`/usr/bin/which $EUCLID_POST_SCRIPT.sh`
        if [[ -r ${epostscr} ]]; then
          . ${epostscr} "$@"
          export EUCLID_POST_DONE=yes
        fi
        unset epostscr
      fi
    fi
      
  fi

  export ELOGIN_DONE=yes

fi

