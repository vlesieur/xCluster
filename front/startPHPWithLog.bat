SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & startPHP.bat > %homepath%\log\PHP.log 2>&1
