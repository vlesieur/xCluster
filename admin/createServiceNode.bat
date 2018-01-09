SET homepath=%cd%
SET batpath="%homepath%\front\start.bat"
sc.exe create "XCluster_Client" binPath="C:\Windows\system32\cmd.exe --"%batpath%" displayname= "XCluster NodeJS Server" start= "auto"
sc.exe description "XCluster_Client" "Client used by XCluster application to request XCluster Python Flask API server"
pause