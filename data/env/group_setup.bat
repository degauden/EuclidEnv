IF DEFINED HOME (
  IF NOT EXIST %HOME%\.noLHCBLoginscript (
    set lbvers3="prod"
    IF EXIST %HOME%\.devLHCBLoginscript (
      set lbvers3="dev"
    )
    IF DEFINED VO_LHCB_SW_DIR (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers3}\InstallArea\scripts\LbLogin.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers3}\InstallArea\scripts\LbLogin.bat --silent %*
      ) else (
        IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat (
          call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat --silent %*
        )
      )
    ) ELSE (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea\scripts\LbLogin.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea\scripts\LbLogin.bat --silent %*
      ) else (
        IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat (
          call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat --silent %*
        )
      )
    )
    set lbvers3=
  )
) ELSE (
  set lbvers3="prod"
  IF DEFINED VO_LHCB_SW_DIR (
    IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers3}\InstallArea\scripts\LbLogin.bat (
      call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\${lbvers3}\InstallArea\scripts\LbLogin.bat --silent %*
    ) else (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\LbLogin.bat --silent %*
      )
    )
  ) ELSE (
    IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea\scripts\LbLogin.bat (
      call /opt/LHCb/lib/lhcb/LBSCRIPTS/${lbvers3}/InstallArea\scripts\LbLogin.bat --silent %*
    ) else (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\LbLogin.bat --silent %*
      )
    )
  )
  set lbvers3=
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


