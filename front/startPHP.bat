TITLE XCLUSTER_PHP
SET mypath=%~dp0
cd %mypath%
%SystemRoot%\System32\where.exe /q php
IF ERRORLEVEL 1 (
	echo "Veuillez renseigner l'emplacement du dossier contenant PHP dans la variable d'environnement du systeme PATH."
	wscript "setPHPenv.vbs"
) ELSE (
	cd %mypath%angular-seed/app
	echo --------------------
	echo Configuration de PHP
	echo --------------------
	echo Vous pouvez utiliser la commande php -i pour verifier votre configuration globale de PHP
	php -r "echo 'upload_max_filesize : '.ini_get('upload_max_filesize');"
	echo .
	php -r "echo 'post_max_size : '.ini_get('post_max_size');"
	echo .
	echo ----------------
	echo Demarrage de PHP
	echo ----------------
	php -S localhost:8000
	@echo off
	pause
)