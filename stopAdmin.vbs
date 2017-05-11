Dim WShell, UAC, SystemRoot, script
Set UAC = CreateObject("Shell.Application") 
Set WShell = CreateObject("WScript.Shell")
script = WShell.CurrentDirectory & "\stop.bat"
Set WShell = Nothing
UAC.ShellExecute script, "1", "", "runas", 1 
