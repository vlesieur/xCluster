TITLE XCLUSTER_SERVER
SET mypath=%~dp0
cd %mypath%
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:Admin
easy_install pip & pip install flask & python server.py
GOTO Next
:NotAdmin
python server.py
GOTO Next
:Next
@echo off
pause

