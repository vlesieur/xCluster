SET homepath=%cd%
SET pythonbinpath="C:\ProgramData\Anaconda3\python.exe"
SET flaskpath="%homepath%\server\flask"
sc.exe create "XCluster_Server" binPath="%pythonbinpath% --"%flaskpath%\manage.py runserver" displayname= "XCluster Python Flask Server" start= "auto"
sc.exe description "XCluster_Server" "Python Flask server used by XCluster application"
pause