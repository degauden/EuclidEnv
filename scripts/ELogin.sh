# main login script for the Euclid environment

my_own_prefix="%(this_install_prefix)s"
python_loc=`python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='$my_own_prefix'))"`

if [[ -r ${python_loc}/Euclid/Login.py ]]; then
  ELogin_tmpfile=`python ${python_loc}/Euclid/Login.py --shell=sh --mktemp "$@"`
  ELoginStatus="$?"  
else
  ELogin_tmpfile=`python -m Euclid.Login --shell=sh --mktemp "$@"`
  ELoginStatus="$?"
fi

unset my_own_prefix
unset python_loc

if [[ "$ELoginStatus" = 0 && -n "$ELogin_tmpfile" ]]; then
  . $ELogin_tmpfile
fi

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

$(exit $ELoginStatus)
