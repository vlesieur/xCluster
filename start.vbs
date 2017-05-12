Dim oWShell, arg, myPath, cpt, sys32
Set oWShell = CreateObject("Wscript.Shell")
SystemRoot = oWShell.expandEnvironmentStrings("%SystemRoot%")
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
Wscript.Sleep 1000
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\start.bat" & arg
Wscript.Sleep 100
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWShell.Run myPath & "\front\startPHP.bat" & arg
cpt = 1
'Attend jusqu à une minute pour lancer le site web
Do While ( GetProcessId("cmd.exe","XCLUSTER_FRONT*") < 1 OR GetProcessId("cmd.exe","XCLUSTER_CLIENT*") < 1 ) AND cpt < 60
Wscript.Sleep 1000
cpt = cpt + 1
Loop
Set oWSHell = Nothing
Set oWShell = CreateObject("Wscript.Shell")
oWshell.Run "http://localhost:8000/"
Set oWSHell = Nothing

Function GetProcessId(imageName, windowTitle)
    Dim currentUser, command, output, tasklist, tasks, i, cols

    currentUser = CreateObject("Wscript.Network").UserName
	
    command = SystemRoot & "\system32\tasklist.exe /V /FO csv"
    command = command & " /FI ""USERNAME eq " + currentUser + """"
    command = command & " /FI ""IMAGENAME eq " + imageName + """"
    command = command & " /FI ""WINDOWTITLE eq " + windowTitle + """"
    command = command & " /FI ""SESSIONNAME eq Console"""

    output = Trim(Shell(command))
    tasklist = Split(output, vbNewLine)

    ' starting at 1 skips first line (it contains the column headings only)
    For i = 1 To UBound(tasklist) - 1
        cols = Split(tasklist(i), """,""")
        ' a line is expected to have 9 columns (0-8)
        If UBound(cols) = 8 Then
            GetProcessId = Trim(cols(1))
            Exit For
        End If
    Next
End Function

Function Shell(cmd)
	Dim fileOutput, openTextFile, strOutput, fso
	fileOutput = mypath & "out.txt"
	WScript.CreateObject("WScript.Shell").Run "cmd /c " & cmd & " > " & fileOutput, 0, True

	' Read the output and remove the file when done...
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set openTextFile = fso.OpenTextFile(fileOutput)
	If Not openTextFile.AtEndOfStream Then strOutput = openTextFile.ReadAll Else strOutput = "" End If
	openTextFile.Close
	fso.DeleteFile fileOutput

	Shell = strOutput
    ' Shell = WScript.CreateObject("WScript.Shell").Exec(cmd).StdOut.ReadAll()
End Function