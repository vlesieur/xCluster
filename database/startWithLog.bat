SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & start.bat > %homepath%\log\MongoDB.log 2>&1
