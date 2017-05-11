Dim oWShell, arg, myPath
Set oWShell = CreateObject("Wscript.Shell")
myPath = replace( WScript.ScriptFullName, WScript.ScriptName, "" )
If oWShell.CurrentDirectory & "\" = myPath Then arg="" Else arg=" ""1""" End If
oWShell.CurrentDirectory = myPath
oWShell.Run myPath & "\database\start.bat" & arg
Wscript.Sleep 1000
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\server\start.bat" & arg
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\client\start.bat" & arg
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\start.bat" & arg
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\startPHP.bat" & arg
Wscript.Sleep 1000
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWshell.Run "http://localhost:8000/"
Set oWSHell = Nothing
