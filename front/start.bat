TITLE XCLUSTER_FRONT
SET mypath=%~dp0
cd %mypath%angular-seed/app/bower_components/angular-filemanager/ & gulp build & cd %mypath%angular-seed/ & npm start
@echo off
pause