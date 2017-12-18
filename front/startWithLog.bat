SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & start.bat > %homepath%\log\angular.log 2>&1
