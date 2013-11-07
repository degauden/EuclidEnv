# main login script for the Euclid environment

set ELogin_tmpfile = `python -m Euclid.Login --shell=csh --mktemp ${*:q}`
set ELoginStatus = $?

if ( ! $ELoginStatus && "$ELogin_tmpfile" != "") then
  source $LbLogin_tmpfile
endif

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

exit $ELoginStatus
