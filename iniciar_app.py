#!/usr/bin/env python3
"""
Inicia a aplicação FastAPI
"""

import subprocess
import sys
import os
import time

def main():
    print("🚀 Iniciando Aplicação")
    print("=" * 30)
    
    # Verifica se está na pasta correta
    if not os.path.exists('app/main.py'):
        print("❌ Execute este script na pasta raiz do projeto")
        return
    
    # Verifica se o venv existe
    venv_python = None
    if os.name == 'nt':  # Windows
        venv_python = os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Linux/Mac
        venv_python = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(venv_python):
        print("❌ Virtual environment não encontrado")
        print("   Execute: python -m venv venv")
        return
    
    print(f"✅ Usando Python: {venv_python}")
    
    # Inicia o servidor com reload e sem auto-restart
    print("✅ Iniciando servidor na porta 8000...")
    print("   Acesse: http://localhost:8000")
    print("   Pressione CTRL+C para parar")
    print("   Servidor ficará rodando continuamente")
    print()
    
    while True:
        try:
            # Usa --reload para recarregar automaticamente
            # Usa --host 0.0.0.0 para aceitar conexões externas
            process = subprocess.Popen([
                venv_python, "-m", "uvicorn", 
                "app.main:app", 
                "--reload", 
                "--host", "0.0.0.0",
                "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Espera o processo terminar (se houver erro, vai terminar)
            stdout, stderr = process.communicate()
            
            # Se houver erro, mostra e tenta novamente
            if process.returncode != 0 and stderr:
                print(f"❌ Erro ao iniciar servidor: {stderr}")
                print("   Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue
            else:
                print("✅ Servidor encerrado normalmente")
                break
                
        except KeyboardInterrupt:
            print("\n✅ Servidor encerrado pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("   Tentando novamente em 5 segundos...")
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()
