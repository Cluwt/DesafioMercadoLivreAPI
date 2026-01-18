@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Iniciando Ngrok
echo ================
echo.

python3 iniciar_ngrok.py
