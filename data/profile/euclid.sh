if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    confscr=`/usr/bin/which Euclid_config.sh`
    . ${confscr} "$@"
    unset confscr
  fi

  # shell part. has to deal with the shell settings. Pretty much everything but 
  # the environment variables. The script can be manually called from .bashrc
  shellscr=`/usr/bin/which Euclid_group_setup.sh`
  if  [[ -e ${shellscr} ]]; then
     . ${shellscr} "$@"
  fi
  unset shellscr

  # login part. has to deal with the environment. The script can be called manually from 
  # .bash_profile
  if (shopt -q login_shell || [[ -o login ]] || [[ -n "$E_BANNER" ]]) 2> /dev/null ; then
    loginscr=`/usr/bin/which Euclid_group_login.sh`
    if [[ -e ${loginscr} ]]; then
       . ${loginscr} "$@"
    fi
    unset loginscr
  fi

fi

