if ( ! -e ${HOME}/.noEuclidLoginScript ) then

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

