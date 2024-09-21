set args=%*
powershell "iex((@('')*3+(cat '%~f0'|select -skip 3))-join[char]10)"


# 再起動するプロセスのパス
$exePath = "C:\Program Files\VIVE\SRanipal\sr_runtime.exe"
$exeName = "sr_runtime.exe"

# プロセス監視と再起動の関数
function Monitor-Process {
    $process = Get-Process -Name $exeName -ErrorAction SilentlyContinue
    if ($process -eq $null) {
        Write-Host "$exeName is not running. Starting it..."
        Start-Process $exePath
    } else {
        Write-Host "$exeName is running."
    }

    Register-WmiEvent -Query "Select * From __InstanceDeletionEvent Within 1 Where TargetInstance ISA 'Win32_Process' And TargetInstance.Name = '$exeName'" -Action {
        Write-Host "$exeName has stopped. Restarting it..."
        Start-Process $exePath
    }
}

# 初回のプロセス監視
Monitor-Process

# スクリプトが終了しないようにするために無限ループを開始
while ($true) {
    Start-Sleep -Seconds 1
}
