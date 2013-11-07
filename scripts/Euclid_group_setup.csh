#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  if ( ! $?EUCLID_CONFIG_FILE ) then
    set confscr=`/usr/bin/which Euclid_config.csh`
    source ${confscr} "${*:q}" >& /dev/null
    unset confscr    
  endif

  set elogscr=`/usr/bin/which Elogin.csh`
  if ( -e ${elogscr} ) then
    
    if ( $?ELOGIN_DONE ) then
      source ${elogscr} --shell-only --silent ${*:q} >& /dev/null
    else
      
      setenv E_BANNER `mktemp`
      source ${elogscr} --quiet ${*:q} >! ${E_BANNER}

      if ( ! $?EUCLID_POST_DONE ) then
        if ( $?EUCLID_POST_SCRIPT ) then
          set epostscr=`/usr/bin/which $EUCLID_POST_SCRIPT.csh`
          if ( -r ${epostscr} ) then
            source ${epostscr} ${*:q} >>! ${E_BANNER}
            setenv EUCLID_POST_DONE yes
          endif
          unset epostscr
        endif
      endif
      
    endif
    
  endif
  unset elogscr

endif

