rem バッチの先頭に記載する
whoami /priv | find "SeDebugPrivilege" > nul
if %errorlevel% neq 0 (
 @powershell start-process %~0 -verb runas
 exit
)


@echo off
taskkill /F /IM VRCFaceTracking.exe
echo タスクが終了しました。

