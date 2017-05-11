SET mypath=%~dp0
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:Admin
cd %mypath%angular-seed/ & bower install & npm install & cd %mypath%angular-seed/app/bower_components/angular-filemanager/ & gulp build & cd %mypath%angular-seed/  & npm start
GOTO Next
:NotAdmin
cd %mypath%angular-seed/app/bower_components/angular-filemanager/ & gulp build & cd %mypath%angular-seed/ & npm start
GOTO Next
:Next
@echo off
pause