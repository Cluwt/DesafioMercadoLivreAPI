@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Executando Testes de Erros
echo ============================
echo.

echo [0/6] Verificando conexão com o servidor...
python verificar_conexao.py
echo.
pause

echo [1/6] Teste de Falha de Autenticação
python test_erro_autenticacao.py
echo.
pause

echo [2/6] Teste de Erros de Requisição
python test_erro_requisicao.py
echo.
pause

echo [3/6] Teste de Mensagens Amigáveis
python test_mensagens_amigaveis.py
echo.
pause

echo [4/6] Teste de Sem Exposição Técnica
python test_sem_exposicao_tecnica.py
echo.
pause

echo [5/6] Teste de Interface de Erros
python test_interface_erros.py
echo.
pause

echo.
echo ✅ Todos os testes concluídos!
pause
