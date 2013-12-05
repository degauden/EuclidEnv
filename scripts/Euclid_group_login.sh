#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  my_own_prefix="%(this_install_prefix)s"

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    if [[ -r ${my_own_prefix}/bin/Euclid_config.sh ]]; then
      confscr=${my_own_prefix}/bin/Euclid_config.sh
    else
      confscr=`/usr/bin/which Euclid_config.sh`
    fi
    . ${confscr} "$@"
    unset confscr
  fi

  if [[ -n "$E_BANNER" ]]; then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unset E_BANNER
  else
    
    if [[ -r ${my_own_prefix}/bin/ELogin.sh ]]; then
      elogscr=${my_own_prefix}/bin/ELogin.sh
    else
      elogscr=`/usr/bin/which ELogin.sh`
    fi    
    if [[ -e ${elogscr} ]]; then
      . ${elogscr} --quiet "$@"
    fi

    if [[ ! -n "$EUCLID_POST_DONE" ]]; then
      if [[ -n "$EUCLID_POST_SCRIPT" ]]; then
        if [[ -r ${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.sh ]]; then
          epostscr=${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.sh
        else
          epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.sh`
        fi
        if [[ -r ${epostscr} ]]; then
          . ${epostscr} "$@"
          export EUCLID_POST_DONE=yes
        fi
        unset epostscr
      fi
    fi
      
  fi

  if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then

    if [[ -r ${my_own_prefix}/bin/StripPath.sh ]]; then
      stripscr=${my_own_prefix}/bin/StripPath.sh
    else
      stripscr=`/usr/bin/which StripPath.sh`
    fi

    . ${stripscr}

    unset stripscr
  
  fi

  export ELOGIN_DONE=yes

  unset my_own_prefix

fi

