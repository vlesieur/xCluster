Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\server\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\client\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\front\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWshell.Run "http://localhost:8000/"
