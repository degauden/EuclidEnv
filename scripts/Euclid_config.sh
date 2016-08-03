# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default
# 4) /etc/default/Euclid
# 5) /etc/sysconfig/euclid

my_own_prefix0="%(this_etc_install_prefix)s"
my_own_exe_prefix0="%(this_install_prefix)s"

# default values if no config file is found
export SOFTWARE_BASE_VAR=EUCLID_BASE
export EUCLID_BASE=%(this_euclid_base)s
export EUCLID_USE_BASE=no
export EUCLID_USE_PREFIX=no


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
cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/euclid"
cfgfiles="$cfgfiles /etc/default/Euclid"
cfgfiles="$cfgfiles /etc/sysconfig/euclid"


for c in $(echo $cfgfiles)
do
  if [[ -r $c ]]; then
    export EUCLID_CONFIG_FILE=$c
    eval `cat $EUCLID_CONFIG_FILE | sed -n -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/\1="\2"; export \1;/gp'`
    break;
  fi
done

unset c
unset cfgfiles

arch_type=`uname -m`

# prepend path entries from the base to the environment
if [[ "${EUCLID_USE_BASE}" == "yes" ]]; then
  if [[ -d ${EUCLID_BASE} ]]; then
    
    if [[ -d ${EUCLID_BASE}/bin ]]; then
      export PATH=${EUCLID_BASE}/bin:${PATH}
    fi
    if [[ -d ${EUCLID_BASE}/scripts ]]; then
      export PATH=${EUCLID_BASE}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_BASE}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib32
        fi
      fi
    fi
    if [[ -d ${EUCLID_BASE}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${EUCLID_BASE}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${EUCLID_BASE}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_BASE}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib64
        fi
      fi
    fi

    
    if [[ -d ${EUCLID_BASE}/python ]]; then
      my_python_base=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_BASE}'))")
      if [[ -d ${my_python_base} ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${my_python_base}:${PYTHONPATH}
        else
          export PYTHONPATH=${my_python_base}
        fi
      else
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${EUCLID_BASE}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${EUCLID_BASE}/python
        fi
      fi
      unset my_python_base
    fi
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}
    fi
    if [[ -d ${EUCLID_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}/cmake:${CMAKE_PREFIX_PATH}
    fi
    
  fi
fi

# prepend path entries from the prefix to the environment
if [[ "${EUCLID_USE_PREFIX}" == "yes" ]]; then
 if [[ -d ${my_own_exe_prefix0} ]]; then

 fi
fi

unset arch_type
unset my_own_prefix0
unset my_own_exe_prefix0

