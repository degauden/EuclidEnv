# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default (if XDG_CONFIG_DIRS exists)
# 4) /etc/default/Euclid
# 5) /etc/sysconfig/euclid

set my_own_prefix0 = "%(this_etc_install_prefix)s"
set my_own_exe_prefix0 = "%(this_install_prefix)s"


# default values if no config file is found
setenv SOFTWARE_BASE_VAR EUCLID_BASE
setenv EUCLID_BASE %(this_euclid_base)s
setenv EUCLID_USE_BASE no
setenv EUCLID_USE_PREFIX no


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
set cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/euclid"
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

set arch_type=`uname -m`

# prepend path entries from the base to the environment 
if ( "${EUCLID_USE_BASE}" == "yes" ) then
  if ( -d ${EUCLID_BASE} ) then

    if ( -d ${EUCLID_BASE}/bin ) then
      setenv PATH ${EUCLID_BASE}/bin:${PATH}
    endif
    if ( -d ${EUCLID_BASE}/scripts ) then
      setenv PATH ${EUCLID_BASE}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_BASE}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib32        
        endif
      endif
    endif
    if ( -d ${EUCLID_BASE}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_BASE}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib64        
        endif
      endif
    endif
    
    if ( -d ${EUCLID_BASE}/python ) then
      set my_python_base = `python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_BASE}'))"`

      if ( -d ${my_python_base} ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
        else
          setenv PYTHONPATH ${my_python_base}        
        endif       
      else
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${EUCLID_BASE}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${EUCLID_BASE}/python        
        endif
      endif  
      unset my_python_base
    endif
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}        
    endif
    if ( -d ${EUCLID_BASE}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}/cmake:${CMAKE_PREFIX_PATH}
    endif                
            
  endif
endif

# prepend path entries from the prefix to the environment 
if ( "${EUCLID_USE_PREFIX}" == "yes" ) then
 if ( -d ${my_own_exe_prefix0} ) then

 endif
endif

unset arch_type
unset my_own_prefix0
unset my_own_exe_prefix0

