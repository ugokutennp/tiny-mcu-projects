rem バッチの先頭に記載する
whoami /priv | find "SeDebugPrivilege" > nul
if %errorlevel% neq 0 (
 @powershell start-process %~0 -verb runas
 exit
)


@echo off
taskkill /F /IM sr_runtime.exe
taskkill /F /IM SRanipalService.exe
echo タスクが終了しました。

