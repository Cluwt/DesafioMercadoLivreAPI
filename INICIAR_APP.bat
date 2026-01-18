@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Iniciando Aplicação
echo ===================
echo.

python3 iniciar_app.py
