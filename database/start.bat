TITLE XCLUSTER_DB
SET mypath=%~dp0
cd %mypath%
MongoDB\Server\3.4\bin\mongod.exe --dbpath "%mypath%MongoDB\Server\3.4\data\db"
@echo off
pause

