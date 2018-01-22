SET mypath=%~dp0
cd /d %mypath%
cd ..
SET homepath=%cd%
SET mongobinpath=%homepath%\database\MongoDB\Server\3.4\bin\mongod.exe
SET mongocfgpath=%homepath%\database\MongoDB\Server\3.4\data\mongod.cfg
sc create "XCluster_Database" binPath= "%mongobinpath% --service --config=%mongocfgpath%" displayName= "XCluster MongoDB Database" start= "demand"
sc description "XCluster_Database" "Database Engine used by XCluster application"
pause