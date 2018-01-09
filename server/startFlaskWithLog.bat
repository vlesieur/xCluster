SET homepath=%cd%
SET mypath=%~dp0
cd %mypath% & python flask/manage.py runserver & start.bat > %homepath%\log\python.log 2>&1
