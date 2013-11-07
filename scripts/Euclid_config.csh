# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default (if XDG_CONFIG_DIRS exists)
# 4) /etc/default/Euclid
# 5) /etc/sysconfig/euclid

# default values if no config file is found
setenv EUCLID_BASE /opt/Euclid
setenv EUCLID_USE_BASE no


set cfgfiles=""
if ( $?XDG_CONFIG_HOME ) then
  set cfgfiles="$cfgfiles $XDG_CONFIG_HOME/Euclid/default"
endif
if ( $?HOME ) then
  set cfgfiles="$cfgfiles $HOME/.config/Euclid/default"
endif

if ( $?XDG_CONFIG_DIRS ) then
  foreach d (`echo $XDG_CONFIG_DIRS | tr -s ':' ' ' `)
    set cfgfiles="$cfgfiles $d/Euclid/default"
  end
  unset d
endif
set cfgfiles="$cfgfiles /etc/default/Euclid"
set cfgfiles="$cfgfiles /etc/sysconfig/euclid"

foreach c ( $cfgfiles )
  if ( -r $c ) then
    setenv EUCLID_CONFIG_FILE $c
    eval `cat $EUCLID_CONFIG_FILE | sed -n -e '/^[^+]/s/\(\\\$[^ ]*\)/"\\\\\1"/' -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/setenv \1 \"\2\";/gp'`
    break
  endif
end

unset c
unset cfgfiles

