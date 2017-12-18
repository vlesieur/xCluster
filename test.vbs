Dim oWShell, arg, myPath, cpt, sys32
Set oWShell = CreateObject("Wscript.Shell")
SystemRoot = oWShell.expandEnvironmentStrings("%SystemRoot%")
myPath = replace( WScript.ScriptFullName, WScript.ScriptName, "" )
If oWShell.CurrentDirectory & "\" = myPath Then arg="" Else arg=" ""1""" End If
oWShell.CurrentDirectory = myPath
oWShell.Run myPath & "\database\startWithLog.bat" & arg
Wscript.Sleep 1000
Set oWShell = Nothing