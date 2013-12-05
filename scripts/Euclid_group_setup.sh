#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  my_own_prefix="%(this_install_prefix)s"

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    if [[ -r ${my_own_prefix}/bin/Euclid_config.sh ]]; then
      confscr=${my_own_prefix}/bin/Euclid_config.sh
    else
      confscr=`/usr/bin/which Euclid_config.sh`
    fi
    . ${confscr} "$@" > /dev/null 2>&1
    unset confscr
  fi

  if [[ -r ${my_own_prefix}/bin/ELogin.sh ]]; then
    elogscr=${my_own_prefix}/bin/ELogin.sh
  else
    elogscr=`/usr/bin/which ELogin.sh`
  fi    
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
          if [[ -r ${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.sh ]]; then
            epostscr=${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.sh
          else
            epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.sh`
          fi
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
  
  
  if [[ -r ${my_own_prefix}/bin/StripPath.sh ]]; then
    stripscr=${my_own_prefix}/bin/StripPath.sh
  else
    stripscr=`/usr/bin/which StripPath.sh`
  fi

  . ${stripscr}

  unset stripscr

  
  unset my_own_prefix

fi

