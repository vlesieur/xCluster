cd /d %systemroot%/system32
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_CLIENT "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_PHP "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_SERVER "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq XCLUSTER_DB "
taskkill.exe /IM cmd.exe /FI "WINDOWTITLE eq bower "