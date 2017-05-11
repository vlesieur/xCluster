TITLE XCLUSTER_CLIENT
SET mypath=%~dp0
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:Admin
cd %mypath%api & npm install --global --production windows-build-tools & npm config set msvs_version 2015 & npm install -g bower & npm install bcrypt & npm install node-gyp & npm install zerorpc & npm install zmq & node app.js
GOTO Next
:NotAdmin
cd %mypath%api & node app.js
GOTO Next
:Next
@echo off
pause