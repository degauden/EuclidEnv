# main login script for the Euclid environment


set my_own_prefix = "%(this_install_prefix)s"

set python_loc = `python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='$my_own_prefix'))"`

if ( -r ${python_loc}/Euclid/Login.py ) then
  set ELogin_tmpfile = `python ${python_loc}/Euclid/Login.py --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?  
else
  set ELogin_tmpfile = `python -m Euclid.Login --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?
endif

unset my_own_prefix
unset python_loc

set needs_cleanup = no

if ( ! $ELoginStatus && "$ELogin_tmpfile" != "") then
  source $LbLogin_tmpfile
  set needs_cleanup = yes
endif

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

if ( "$needs_cleanup" == "yes" ) then
  if (! ${?E_NO_STRIP_PATH} ) then

    if ( -r ${my_own_prefix}/bin/StripPath.csh ) then
      set stripscr=${my_own_prefix}/bin/StripPath.csh
    else
      set stripscr=`/usr/bin/which StripPath.csh`
    endif
  
    source ${stripscr}
  
    unset stripscr

  endif
endif

unset needs_cleanup

exit $ELoginStatus
