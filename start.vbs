Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\server\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run ".\client\start.bat"
Set oWSHell = Nothing
