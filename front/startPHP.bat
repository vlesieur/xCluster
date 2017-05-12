TITLE XCLUSTER_PHP
SET mypath=%~dp0
cd %mypath%angular-seed/app
%SystemRoot%\System32\where.exe /q php

	echo --------------------
	echo Configuration de PHP
	echo --------------------
	echo Vous pouvez utiliser la commande php -i pour verifier votre configuration globale de PHP
	C:\wamp64\bin\php\php7.0.10\php.exe -r "echo 'upload_max_filesize : '.ini_get('upload_max_filesize');"
	echo .
	echo ----------------
	echo Demarrage de PHP
	echo ----------------
    C:\wamp64\bin\php\php7.0.10\php.exe -S localhost:8000

@echo off
pause