#!/bin/sh
if [[ ! -e ${HOME}/.noLHCBLoginscript ]]; then


# default file to be tested in order
# 1) $XDG_CONFIG_HOME/LHCb/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/LHCb/default
# 3) for f in $XDG_CONFIG_DIRS : $f/LHCb/default
# 4) /etc/default/LHCb

cfgfiles=""
if [[  -n "$XDG_CONFIG_HOME" ]]; then
  cfgfiles="$cfgfiles $XDG_CONFIG_HOME/LHCb/default"
fi
if [[ -n "$HOME" ]]; then
  cfgfiles="$cfgfiles $HOME/.config/LHCb/default"
fi

if [[ -n "$XDG_CONFIG_DIRS" ]]; then
  for d in $(echo $XDG_CONFIG_DIRS | tr -s ':' ' ')
  do
    cfgfiles="$cfgfiles $d/LHCb/default"
  done
  unset d
fi
cfgfiles="$cfgfiles /etc/default/LHCb"
cfgfiles="$cfgfiles /etc/xdg/LHCb/default"


for c in $cfgfiles
do
  if [[ -r $c ]]; then
    eval `cat $c | sed -n -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/\1="\2"; export \1;/gp'`
    break;
  fi
done

unset c
unset cfgfiles

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

