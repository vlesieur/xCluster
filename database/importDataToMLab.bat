SET mypath=%~dp0
cd %mypath%
MongoDB\Server\3.4\bin\mongoimport.exe -h ds050869.mlab.com:50869 -d bd_films -c users -u xcluster -p xcluster --file %mypath%test.json
@echo off
pause

