#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  set my_own_prefix = "%(this_install_prefix)s"

  if ( ! $?EUCLID_CONFIG_FILE ) then
    if ( -r ${my_own_prefix}/bin/Euclid_config.csh ) then
      set confscr=${my_own_prefix}/bin/Euclid_config.csh
    else
      set confscr=`/usr/bin/which Euclid_config.csh`        
    endif
    source ${confscr} "${*:q}"
    unset confscr    
  endif

  if ( $?E_BANNER ) then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unsetenv E_BANNER
  else

    if ( -r ${my_own_prefix}/bin/ELogin.csh ) then
      set elogscr=${my_own_prefix}/bin/ELogin.csh
    else
      set elogscr=`/usr/bin/which ELogin.csh`        
    endif
    if ( -e ${elogscr} ) then
      source ${elogscr} --quiet ${*:q}
    endif

    if ( ! $?EUCLID_POST_DONE ) then
      if ( $?EUCLID_POST_SCRIPT ) then
        if ( -r ${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.csh ) then
          set epostscr=${my_own_prefix}/bin/${EUCLID_POST_SCRIPT}.csh
        else
          set epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.csh`        
        endif
        if ( -r ${epostscr} ) then
          source ${epostscr} ${*:q}
          setenv EUCLID_POST_DONE yes
        endif
        unset epostscr
      endif
    endif
  
  endif


  if ( -r ${my_own_prefix}/bin/StripPath.csh ) then
    set stripscr=${my_own_prefix}/bin/StripPath.csh
  else
    set stripscr=`/usr/bin/which StripPath.csh`        
  endif
  
  source ${stripscr}
  
  unset stripscr

                            
  setenv ELOGIN_DONE yes

  unset my_own_prefix

endif

