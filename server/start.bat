TITLE XCLUSTER_SERVER
SET mypath=%~dp0
cd %mypath%
easy_install pip & pip install flask & python server.py
@echo off
pause

