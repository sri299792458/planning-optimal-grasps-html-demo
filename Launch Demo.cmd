@echo off
setlocal

set "PORT=8765"
set "ROOT=%~dp0"
set "URL=http://127.0.0.1:%PORT%/"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$client = New-Object Net.Sockets.TcpClient; try { $client.Connect('127.0.0.1', %PORT%); exit 0 } catch { exit 1 } finally { if ($client) { $client.Dispose() } }"

if errorlevel 1 (
  start "Planning Optimal Grasps Demo Server" /min cmd /c "cd /d ""%ROOT%"" && python -m http.server %PORT%"
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Sleep -Milliseconds 1200"
)

start "" "%URL%"

endlocal
