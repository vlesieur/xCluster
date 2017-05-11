TITLE XCLUSTER_CLIENT
SET mypath=%~dp0
cd %mypath%api & npm install --global --production windows-build-tools & npm config set msvs_version 2015 & npm install -g bower & npm install node-gyp & npm install zerorpc & npm install zmq & node app.js
@echo off
pause