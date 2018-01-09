cd /d %systemroot%/system32
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:NotAdmin
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_SERVER"
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_DB"
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_FRONT"
GOTO Next
:Admin
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq Admin*"
GOTO Next
:Next
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER*"