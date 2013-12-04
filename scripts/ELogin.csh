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

if ( ! $ELoginStatus && "$ELogin_tmpfile" != "") then
  source $LbLogin_tmpfile
endif

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

exit $ELoginStatus
