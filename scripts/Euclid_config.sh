# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default
# 4) /etc/default/Euclid
# 5) /etc/sysconfig/euclid

# default values if no config file is found
export EUCLID_BASE=/opt/Euclid
export EUCLID_USE_BASE=no


cfgfiles=""
if [[  -n "$XDG_CONFIG_HOME" ]]; then
  cfgfiles="$cfgfiles $XDG_CONFIG_HOME/Euclid/default"
fi
if [[ -n "$HOME" ]]; then
  cfgfiles="$cfgfiles $HOME/.config/Euclid/default"
fi

if [[ -n "$XDG_CONFIG_DIRS" ]]; then
  for d in $(echo $XDG_CONFIG_DIRS | tr -s ':' ' ')
  do
    cfgfiles="$cfgfiles $d/Euclid/default"
  done
  unset d
fi
cfgfiles="$cfgfiles /etc/default/Euclid"
cfgfiles="$cfgfiles /etc/sysconfig/euclid"


for c in $cfgfiles
do
  if [[ -r $c ]]; then
    export EUCLID_CONFIG_FILE=$c
    eval `cat $EUCLID_CONFIG_FILE | sed -n -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/\1="\2"; export \1;/gp'`
    break;
  fi
done

unset c
unset cfgfiles
