TITLE XCLUSTER_SERVER
SET mypath=%~dp0
cd %mypath%
python flask/manage.py runserver
@echo off
pause

