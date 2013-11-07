if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_SYS_CONFIG" ]]; then
    export EUCLID_SYS_CONFIG=/etc/sysconfig/euclid
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
  if (shopt -q login_shell || [[ -o login ]]) 2> /dev/null ; then
    loginscr=`/usr/bin/which Euclid_group_login.sh`
    if [[ -e ${loginscr} ]]; then
       . ${loginscr} "$@"
    fi
    unset loginscr
  fi

fi


if [[ ! -n "$VO_LHCB_SW_DIR" ]]; then
  export VO_LHCB_SW_DIR=/opt/LHCb
fi

if [[ ! -e ${HOME}/.noLHCBLoginscript ]]; then
  lbvers=prod
  if [[ -e ${HOME}/.devLHCBLoginscript ]]; then
    lbvers=dev
  fi
  if [[ -n "$VO_LHCB_SW_DIR" ]]; then
    if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.sh ]]; then
      . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.sh  "$@"
    else
      if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.sh ]]; then
        . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.sh  "$@"
      fi
    fi
  else
    if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.sh ]]; then
      . /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.sh  "$@"
    else
      if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.sh ]]; then
        . /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.sh  "$@"
      fi
    fi
  fi
  if (shopt -q login_shell || [[ -o login ]] || [[ -n "$LB_BANNER" ]]) 2> /dev/null ; then
    if [[ -n "$VO_LHCB_SW_DIR" ]]; then
      if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.sh ]]; then
        . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.sh  "$@"
      else
        if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.sh ]]; then
          . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.sh  "$@"
        fi
      fi
    else
      if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.sh ]]; then
        . /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.sh  "$@"
      else
        if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.sh ]]; then
          . /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.sh  "$@"
        fi
      fi
    fi
  fi
  unset lbvers
fi
