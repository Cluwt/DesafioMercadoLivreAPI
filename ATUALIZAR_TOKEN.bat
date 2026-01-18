@echo off
chcp 65001 >nul
cd /d "%~dp0"
python3 atualizar_token.py
pause
