Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\start.bat", 0, False
Wscript.Sleep 1000
oWshell.Run "http://localhost:3000/"
Set oWSHell = Nothing
