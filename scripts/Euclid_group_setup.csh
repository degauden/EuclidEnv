#!/bin/csh
if ( ! -e ${HOME}/.noLHCBLoginscript ) then


# default file to be tested in order
# 1) $XDG_CONFIG_HOME/LHCb/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/LHCb/default
# 3) for f in $XDG_CONFIG_DIRS : $f/LHCb/default (if XDG_CONFIG_DIRS exists)
# 4) /etc/default/LHCb

set cfgfiles=""
if ( $?XDG_CONFIG_HOME ) then
  set cfgfiles="$cfgfiles $XDG_CONFIG_HOME/LHCb/default"
endif
if ( $?HOME ) then
  set cfgfiles="$cfgfiles $HOME/.config/LHCb/default"
endif

if ( $?XDG_CONFIG_DIRS ) then
  foreach d (`echo $XDG_CONFIG_DIRS | tr -s ':' ' ' `)
    set cfgfiles="$cfgfiles $d/LHCb/default"
  end
  unset d
endif
set cfgfiles="$cfgfiles /etc/default/LHCb"
set cfgfiles="$cfgfiles /etc/xdg/LHCb/default"

foreach c ( $cfgfiles )
  if ( -r $c ) then
    eval `cat $c | sed -n -e '/^[^+]/s/\(\\\$[^ ]*\)/"\\\\\1"/' -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/setenv \1 \"\2\";/gp'`
    break
  endif
end

unset c
unset cfgfiles

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

