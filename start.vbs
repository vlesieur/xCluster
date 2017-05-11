Dim oWShell, oArgs, myPath
Set oWShell = CreateObject("Wscript.Shell")
myPath = replace( WScript.ScriptFullName, WScript.ScriptName, "" )
oWShell.CurrentDirectory = myPath
oWShell.Run myPath & "\database\start.bat"
Wscript.Sleep 1000
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\server\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\client\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\start.bat"
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\startPHP.bat"
Wscript.Sleep 1000
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWshell.Run "http://localhost:8000/"
Set oWSHell = Nothing
