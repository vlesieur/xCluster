Dim wShell, fso, PHP_DIRECTORY, sFileSelected , oExec, strPath, UAC, SystemRoot, cscript, start, myPath
If WScript.Arguments.length = 0 Then
	Set UAC = CreateObject("Shell.Application") 
	Set WShell = CreateObject("WScript.Shell")
	SystemRoot = WShell.expandEnvironmentStrings("%SystemRoot%")
	cscript = SystemRoot & "\System32\cscript.exe"
	start = WScript.ScriptFullName
	Set WShell = Nothing
	UAC.ShellExecute cscript, Chr(34) & start & Chr(34) & " uac", "", "runas", 1 
Else
	Set WShell=CreateObject("WScript.Shell")
	Set oExec=WShell.Exec("mshta.exe ""about:<input type=file id=FILE><script>FILE.click();new ActiveXObject('Scripting.FileSystemObject').GetStandardStream(1).WriteLine(FILE.value);close();resizeTo(0,0);</script>""")
	sFileSelected = oExec.StdOut.ReadLine
	Set fso = CreateObject("Scripting.FileSystemObject") 
	PHP_DIRECTORY = "" & fso.GetParentFolderName(sFileSelected)
	If PHP_DIRECTORY = "" Then
		WShell = Nothing
	Else
		strPath = WShell.RegRead("HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\Path")
		strPath=Replace(strPath,";" & PHP_DIRECTORY,"")
		strPath= "" & strPath & ";" & PHP_DIRECTORY
		strPath=Replace(strPath,";;",";")
		strPath=Replace(strPath,";;;",";")
		WShell.RegWrite "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\Path", strPath
		SystemRoot = WShell.expandEnvironmentStrings("%SystemRoot%")
		myPath = replace( WScript.ScriptFullName, WScript.ScriptName, "" )
		WShell.CurrentDirectory = myPath
		WShell.Run myPath & "\startPHP.bat"
		WShell = Nothing
	End If
End If
