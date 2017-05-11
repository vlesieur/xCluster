cd /d %systemroot%/system32
if [%1]==[] GOTO NotAdmin
if [%1]==[1] GOTO Admin
:NotAdmin
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_CLIENT "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_PHP "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_SERVER "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_DB "
GOTO Next
:Admin
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq Admin*"
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq npm"
GOTO Next
:Next
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq bower "