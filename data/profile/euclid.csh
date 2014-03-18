if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  set my_own_prefix4 = "%(this_install_prefix)s"

  if ( ! $?EUCLID_CONFIG_FILE ) then
    if ( -r ${my_own_prefix4}/bin/Euclid_config.csh ) then
      set confscr=${my_own_prefix4}/bin/Euclid_config.csh
    else
      set confscr=`/usr/bin/which Euclid_config.csh`        
    endif
    source ${confscr} "${*:q}"
    unset confscr    
  endif
  
  # shell part. has to deal with the shell settings. Pretty much everything but 
  # the environment variables. The script can be manually called from .tcshrc
  if ( -r ${my_own_prefix4}/bin/Euclid_group_setup.csh ) then
    set shellscr=${my_own_prefix4}/bin/Euclid_group_setup.csh
  else
    set shellscr=`/usr/bin/which Euclid_group_setup.csh`        
  endif
  if ( -e ${shellscr} ) then
    source ${shellscr} ${*:q}
  endif
  unset shellscr

  # login part. has to deal with the environment. The script can be called manually from 
  # .login
  if ($?loginsh) then
    if ( -r ${my_own_prefix4}/bin/Euclid_group_login.csh ) then
      set loginscr=${my_own_prefix4}/bin/Euclid_group_login.csh
    else
      set loginscr=`/usr/bin/which Euclid_group_login.csh`        
    endif
    if ( -e ${loginscr} ) then
      source ${loginscr} ${*:q}
    endif
    unset loginscr
  endif
  
  unset my_own_prefix4

endif

