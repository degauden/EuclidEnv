# main login script for the Euclid environment


set my_own_prefix = "%(this_install_prefix)s"

if ( -r $my_own_prefix/python/Euclid/Login.py ) then
  set ELogin_tmpfile = `python $my_own_prefix/python/Euclid/Login.py --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?  
else
  set ELogin_tmpfile = `python -m Euclid.Login --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?
endif

unset my_own_prefix

if ( ! $ELoginStatus && "$ELogin_tmpfile" != "") then
  source $LbLogin_tmpfile
endif

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

exit $ELoginStatus
