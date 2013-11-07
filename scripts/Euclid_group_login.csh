#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  if ( ! $?EUCLID_CONFIG_FILE ) then
    set confscr=`/usr/bin/which Euclid_config.csh`
    source ${confscr} "${*:q}"
    unset confscr    
  endif

  set lbvers2=prod
  if ( -e ${HOME}/.devLHCBLoginscript ) then
    set lbvers2=dev
  endif
  if ( $?LB_BANNER ) then
    cat ${LB_BANNER}
    rm -f ${LB_BANNER}
    unsetenv LB_BANNER
  else
    if ( $?VO_LHCB_SW_DIR ) then
      if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.csh ) then
        source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.csh --quiet ${*:q}
      else
        if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --quiet ${*:q}
        endif
      endif
    else
      if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.csh ) then
        source /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea/scripts/LbLogin.csh --quiet ${*:q}
      else
        if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh ) then
          source /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/LbLogin.csh --quiet ${*:q}
        endif
      endif
    endif
  endif
  setenv LBLOGIN_DONE yes
  unset lbvers2


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

