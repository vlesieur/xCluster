TITLE XCLUSTER_SERVER
SET mypath=%~dp0
cd %mypath%
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:Admin
pip install django==1.11 & python flask/manage.py runserver
GOTO Next
:NotAdmin
python flask/manage.py runserver
GOTO Next
:Next
@echo off
pause

