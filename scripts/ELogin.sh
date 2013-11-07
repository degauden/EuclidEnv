# main login script for the Euclid environment

ELogin_tmpfile=`python -m Euclid.Login --shell=sh --mktemp "$@"`
ELoginStatus="$?"

if [[ "$ELoginStatus" = 0 && -n "$ELogin_tmpfile" ]]; then
  . $ELogin_tmpfile
fi

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

$(exit $ELoginStatus)
