if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then
  StripPath_tmpfile=`python -m Euclid.PathStripper --shell=sh --mktemp -e PATH -e LD_LIBRARY_PATH -e PYTHONPATH -e HPATH `
  StripPathStatus="$?"
  if [ "$StripPathStatus" = 0 -a -n "$StripPath_tmpfile" ]; then
    . $StripPath_tmpfile
  fi
  rm -f $StripPath_tmpfile
  unset StripPath_tmpfile
  unset E_NO_STRIP_PATH
fi
