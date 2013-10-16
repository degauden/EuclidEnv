IF NOT DEFINED VO_LHCB_SW_DIR (
  set VO_LHCB_SW_DIR=/opt/LHCb
)

IF DEFINED HOME (
  IF NOT EXIST %HOME%\.noLHCBLoginscript (
    set lbvers="prod"
    IF EXIST %HOME%\.devLHCBLoginscript (
      set lbvers="dev"
    )
    IF DEFINED VO_LHCB_SW_DIR (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\%lbvers%\InstallArea\scripts\group_login.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\%lbvers%\InstallArea\scripts\group_login.bat  %*
      ) else (
        IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\group_login.bat (
          call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\group_login.bat  %*
        )
      )
    ) ELSE (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/%lbvers%/InstallArea\scripts\group_login.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/%lbvers%/InstallArea\scripts\group_login.bat  %*
      ) else (
        IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\group_login.bat (
          call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\group_login.bat  %*
        )
      )
    )
    set lbvers=
  )
) ELSE (
  set lbvers="prod"
  IF DEFINED VO_LHCB_SW_DIR (
    IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\%lbvers%\InstallArea\scripts\group_login.bat (
      call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\%lbvers%\InstallArea\scripts\group_login.bat  %*
    ) else (
      IF EXIST %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\group_login.bat (
        call %VO_LHCB_SW_DIR%\lib\lhcb\LBSCRIPTS\LBSCRIPTS_v7r7p1\InstallArea\scripts\group_login.bat  %*
      )
    )
  ) ELSE (
    IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/%lbvers%/InstallArea\scripts\group_login.bat (
      call /opt/LHCb/lib/lhcb/LBSCRIPTS/%lbvers%/InstallArea\scripts\group_login.bat  %*
    ) else (
      IF EXIST /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\group_login.bat (
        call /opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v7r7p1/InstallArea\scripts\group_login.bat  %*
      )
    )
  )
  set lbvers=
)
