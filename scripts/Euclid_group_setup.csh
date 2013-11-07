#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  if ( ! $?EUCLID_CONFIG_FILE ) then
    set confscr=`/usr/bin/which Euclid_config.csh`
    source ${confscr} "${*:q}"
    unset confscr    
  endif

  set lbvers3=prod
  if ( -e ${HOME}/.devLHCBLoginscript ) then
    set lbvers3=dev
  endif
  if ( $?LBLOGIN_DONE ) then
    if ( $?VO_LHCB_SW_DIR ) then
      if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh ) then
        source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh --silent ${*:q} >& /dev/null
      else
        if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --silent ${*:q} >& /dev/null
        endif
      endif
    else
      if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh ) then
        source /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh --silent ${*:q} >& /dev/null
      else
        if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --silent ${*:q} >& /dev/null
        endif
      endif
    endif
  else
    setenv LB_BANNER `mktemp`
    if ( $?VO_LHCB_SW_DIR ) then
      if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh ) then
        source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh --quiet ${*:q} >! ${LB_BANNER}
      else
        if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --quiet ${*:q} >! ${LB_BANNER}
        endif
      endif
    else
      if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh ) then
        source /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea/scripts/LbLogin.csh --quiet ${*:q} >! ${LB_BANNER}
      else
        if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --quiet ${*:q} >! ${LB_BANNER}
        endif
      endif
    endif
  endif
  unset lbvers3


if ( ! $?LHCB_POST_DONE ) then
  if ( $?LHCB_POST_SCRIPT ) then
    if ( -r $LHCB_POST_SCRIPT.csh ) then
      source $LHCB_POST_SCRIPT.csh
      setenv LHCB_POST_DONE yes
    endif
  else
    if ( $?VO_LHCB_SW_DIR ) then
      if ( -r $VO_LHCB_SW_DIR/lib/etc/postscript.csh ) then
        source $VO_LHCB_SW_DIR/lib/etc/postscript.csh
        setenv LHCB_POST_DONE yes
      endif
    endif
  endif
endif


endif

