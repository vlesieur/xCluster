TITLE XCLUSTER_PHP
SET mypath=%~dp0
cd %mypath%angular-seed/app

	echo --------------------
	echo Configuration de PHP
	echo --------------------
	echo Vous pouvez utiliser la commande php -i pour verifier votre configuration globale de PHP
	C:\Users\q.chauvel\MIAGE\PPD\php-7.1.2-Win32-VC14-x64\php.exe -r "echo 'upload_max_filesize : '.ini_get('upload_max_filesize');"
	echo .
	echo ----------------
	echo Demarrage de PHP
	echo ----------------
    C:\Users\q.chauvel\MIAGE\PPD\php-7.1.2-Win32-VC14-x64\php.exe -S localhost:8000

@echo off
pause