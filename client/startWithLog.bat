SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & start.bat > %homepath%\log\api.log 2>&1
