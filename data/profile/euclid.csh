if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  if (! $?EUCLID_SYS_CONFIG ) then
    setenv EUCLID_SYS_CONFIG=/etc/sysconfig/euclid
  endif


  # shell part. has to deal with the shell settings. Pretty much everything but 
  # the environment variables. The script can be manually called from .tcshrc
  set shellscr=`/usr/bin/which Euclid_group_setup.csh`
  if ( -e ${shellscr} ) then
    source ${shellscr} ${*:q}
  endif
  unset shellscr

  # login part. has to deal with the environment. The script can be called manually from 
  # .login
  if ($?loginsh) then
    set loginscr=`/usr/bin/which Euclid_group_login.csh`
    if ( -e ${loginscr} ) then
      source ${loginscr} ${*:q}
    endif
    unset loginscr
  endif

endif


if (! $?VO_LHCB_SW_DIR ) then
  setenv VO_LHCB_SW_DIR /opt/LHCb
endif

if ( ! -e ${HOME}/.noLHCBLoginscript ) then
  set lbvers=prod
  if ( -e ${HOME}/.devLHCBLoginscript ) then
    set lbvers=dev
  endif
  if ( $?VO_LHCB_SW_DIR ) then
    if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.csh ) then
      source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.csh  ${*:q}
    else
      if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.csh ) then
        source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.csh  ${*:q}
      endif
    endif
  else
    if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.csh ) then
      source /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_shell.csh  ${*:q}
    else
      if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.csh ) then
        source /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_shell.csh  ${*:q}
      endif
    endif
  endif
  if ($?loginsh  || $?LB_BANNER) then
    if ( $?VO_LHCB_SW_DIR ) then
      if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.csh ) then
        source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.csh  ${*:q}
      else
        if ( -e ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.csh ) then
          source ${VO_LHCB_SW_DIR}/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.csh  ${*:q}
        endif
      endif
    else
      if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.csh ) then
        source /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers}/InstallArea/scripts/group_login.csh  ${*:q}
      else
        if ( -e /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.csh ) then
          source /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea/scripts/group_login.csh  ${*:q}
        endif
      endif
    endif
  endif
  unset lbvers
endif
