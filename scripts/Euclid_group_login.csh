#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  if ( ! $?EUCLID_CONFIG_FILE ) then
    set confscr=`/usr/bin/which Euclid_config.csh`
    source ${confscr} "${*:q}"
    unset confscr    
  endif

  if ( $?E_BANNER ) then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unsetenv E_BANNER
  else
    
    set elogscr=`/usr/bin/which Elogin.csh`
    if ( -e ${elogscr} ) then
      source ${elogscr} --quiet ${*:q}
    endif

    if ( ! $?EUCLID_POST_DONE ) then
      if ( $?EUCLID_POST_SCRIPT ) then
        set epostscr=`/usr/bin/which $EUCLID_POST_SCRIPT.csh`
        if ( -r ${epostscr} ) then
          source ${epostscr} ${*:q}
          setenv EUCLID_POST_DONE yes
        endif
        unset epostscr
      endif
    endif

  
  endif
  
  setenv ELOGIN_DONE yes


endif

