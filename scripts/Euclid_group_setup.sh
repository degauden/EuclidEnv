#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    confscr=`/usr/bin/which Euclid_config.sh`
    . ${confscr} "$@"
    unset confscr
  fi

  lbvers3=prod
  if [[ -e ${HOME}/.devLHCBLoginscript ]]; then
    lbvers3=dev
  fi
  if [[ -n "$LBLOGIN_DONE" ]]; then
    if [[ -n "$VO_LHCB_SW_DIR" ]]; then
      if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh ]]; then
        . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh --silent "$@" 2>&1 /dev/null
      else
        if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --silent "$@" 2>&1 /dev/null
        fi
      fi
    else
      if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh ]]; then
        . /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh --silent "$@" 2>&1 /dev/null
      else
        if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --silent "$@" 2>&1 /dev/null
        fi
      fi
    fi
  else
    export LB_BANNER=`mktemp`
    if [[ -n "$VO_LHCB_SW_DIR" ]]; then
      if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh ]]; then
        . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh --quiet "$@" >> ${LB_BANNER}
      else
        if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --quiet "$@" >> ${LB_BANNER}
        fi
      fi
    else
      if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh ]]; then
        . /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.sh --quiet "$@" >> ${LB_BANNER}
      else
        if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --quiet "$@" >> ${LB_BANNER}
        fi
      fi
    fi
  fi
  unset lbvers3

if [[ ! -n "$LHCB_POST_DONE" ]]; then
  if [[ -n "$LHCB_POST_SCRIPT" ]]; then
    if [[ -r $LHCB_POST_SCRIPT.sh ]]; then
      . $LHCB_POST_SCRIPT.sh
      export LHCB_POST_DONE=yes
    fi
  else
    if [[ -n "$VO_LHCB_SW_DIR" ]]; then
      if [[ -r $VO_LHCB_SW_DIR/lib/etc/postscript.sh ]]; then
        . $VO_LHCB_SW_DIR/lib/etc/postscript.sh
        export LHCB_POST_DONE=yes
      fi
    fi
  fi
fi



fi

