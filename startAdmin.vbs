Dim WShell, UAC, SystemRoot, cscript, start
Set UAC = CreateObject("Shell.Application") 
Set WShell = CreateObject("WScript.Shell")
SystemRoot = WShell.expandEnvironmentStrings("%SystemRoot%")
cscript = SystemRoot & "\System32\cscript.exe"
start = WShell.CurrentDirectory & "\start.vbs"
Set WShell = Nothing
UAC.ShellExecute cscript, Chr(34) & start & Chr(34), "", "runas", 1 
