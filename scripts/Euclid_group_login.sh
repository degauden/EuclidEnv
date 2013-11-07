#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  if [[ ! -n "$EUCLID_CONFIG_FILE" ]]; then
    confscr=`/usr/bin/which Euclid_config.sh`
    . ${confscr} "$@"
    unset confscr
  fi

  lbvers2=prod
  if [[ -e ${HOME}/.devLHCBLoginscript ]]; then
    lbvers2=dev
  fi
  if [[ -n "$LB_BANNER" ]]; then
    cat ${LB_BANNER}
    rm -f ${LB_BANNER}
    unset LB_BANNER
  else
    if [[ -n "$VO_LHCB_SW_DIR" ]]; then
      if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.sh ]]; then
        . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.sh --quiet "$@"
      else
        if [[ -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --quiet "$@"
        fi
      fi
    else
      if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.sh ]]; then
        . /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.sh --quiet "$@"
      else
        if [[ -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh ]]; then
          . /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.sh --quiet "$@"
        fi
      fi
    fi
  fi
  export LBLOGIN_DONE=yes
  unset lbvers2

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

