SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & start.bat > %homepath%\log\python.log 2>&1
