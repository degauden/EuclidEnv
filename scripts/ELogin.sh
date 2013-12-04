# main login script for the Euclid environment

my_own_prefix="%(this_install_prefix)s"


if [[ -r $my_own_prefix/python/Euclid/Login.py ]]; then
  ELogin_tmpfile=`python $my_own_prefix/python/Euclid/Login.py --shell=sh --mktemp "$@"`
  ELoginStatus="$?"  
else
  ELogin_tmpfile=`python -m Euclid.Login --shell=sh --mktemp "$@"`
  ELoginStatus="$?"
fi

unset my_own_prefix

if [[ "$ELoginStatus" = 0 && -n "$ELogin_tmpfile" ]]; then
  . $ELogin_tmpfile
fi

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

$(exit $ELoginStatus)
