
IF DEFINED HOME (
  IF NOT EXIST %HOME%\.noLHCBLoginscript (
    set lbvers2="prod"
    IF EXIST %HOME%\.devLHCBLoginscript (
      set lbvers2="dev"
    )
    IF DEFINED VO_LHCB_SW_DIR (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers2}\InstallArea\scripts\LbLogin.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers2}\InstallArea\scripts\LbLogin.bat --quiet %*
      ) else (
        IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat (
          call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat --quiet %*
        )
      )
    ) ELSE (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea\scripts\LbLogin.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea\scripts\LbLogin.bat --quiet %*
      ) else (
        IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat (
          call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat --quiet %*
        )
      )
    )
    set lbvers2=
  )
) ELSE (
  set lbvers2="prod"
  IF DEFINED VO_LHCB_SW_DIR (
    IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers2}\InstallArea\scripts\LbLogin.bat (
      call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers2}\InstallArea\scripts\LbLogin.bat --quiet %*
    ) else (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat --quiet %*
      )
    )
  ) ELSE (
    IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea\scripts\LbLogin.bat (
      call /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers2}/InstallArea\scripts\LbLogin.bat --quiet %*
    ) else (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat --quiet %*
      )
    )
  )
  set lbvers2=
)
IF NOT DEFINED LHCB_POST_DONE (
  IF DEFINED LHCB_POST_SCRIPT (
    IF EXIST %LHCB_POST_SCRIPT%.bat (
      call %LHCB_POST_SCRIPT%.bat
      set LHCB_POST_DONE=yes
    )
  ) ELSE (
    IF DEFINED VO_LHCB_SW_DIR (
      IF EXIST %VO_LHCB_SW_DIR%/lib/etc/postscript.bat (
        call %VO_LHCB_SW_DIR%/lib/etc/postscript.bat
        set LHCB_POST_DONE=yes
      )
    )
  )
)


