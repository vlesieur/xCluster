Set UAC = CreateObject("Shell.Application") 
UAC.ShellExecute "start.bat", "", "", "runas", 1 
