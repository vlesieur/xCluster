SET homepath=%cd%
SET mongobinpath="%homepath%\database\MongoDB\Server\3.4\bin"
SET mongodbpath="%homepath%\database\MongoDB\Server\3.4\data\db"
SET mongologpath="%homepath%\log\MongoDB.log"
sc.exe create "XCluster_Database" binPath="%mongobinpath%\mongod.exe --service --config= "%mongobinpath%\mongod.config" displayname= "XCluster MongoDB Database" start= "auto"
sc.exe description "XCluster_Database" "Database Engine used by XCluster application"
pause