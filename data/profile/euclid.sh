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

  # shell part. has to deal with the shell settings. Pretty much everything but 
  # the environment variables. The script can be manually called from .bashrc
  if [[ -r ${my_own_prefix}/bin/Euclid_group_setup.sh ]]; then
    shellscr=${my_own_prefix}/bin/Euclid_group_setup.sh
  else
    shellscr=`/usr/bin/which Euclid_group_setup.sh`
  fi
  if  [[ -e ${shellscr} ]]; then
     . ${shellscr} "$@"
  fi
  unset shellscr

  # login part. has to deal with the environment. The script can be called manually from 
  # .bash_profile
  if (shopt -q login_shell || [[ -o login ]] || [[ -n "$E_BANNER" ]]) 2> /dev/null ; then
    if [[ -r ${my_own_prefix}/bin/Euclid_group_login.sh ]]; then
      loginscr=${my_own_prefix}/bin/Euclid_group_login.sh
    else
      loginscr=`/usr/bin/which Euclid_group_login.sh`
    fi
    if [[ -e ${loginscr} ]]; then
       . ${loginscr} "$@"
    fi
    unset loginscr
  fi

  unset my_own_prefix

fi

