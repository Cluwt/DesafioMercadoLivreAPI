#!/usr/bin/env python3
"""
Inicia ngrok para expor a porta 8000
"""

import subprocess
import sys
import os

def main():
    print("🌐 Iniciando Ngrok")
    print("=" * 25)
    
    # Verifica se o venv existe
    if os.name == 'nt':  # Windows
        venv_python = os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Linux/Mac
        venv_python = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(venv_python):
        print("❌ Virtual environment não encontrado")
        print("   Execute: python -m venv venv")
        return
    
    print(f"✅ Usando Python: {venv_python}")
    
    print("✅ Expondo porta 8000 para internet...")
    print("   Aguarde ngrok gerar URL pública")
    print("   Pressione CTRL+C para parar")
    print("   Ngrok ficará rodando continuamente")
    print()
    
    try:
        # Inicia ngrok sem timeout para manter rodando
        subprocess.run([
            venv_python, "-c", 
            "import subprocess; "
            "import sys; "
            "subprocess.run(['ngrok', 'http', '8000'])"
        ], check=True)
    except KeyboardInterrupt:
        print("\n✅ Ngrok encerrado pelo usuário")
    except FileNotFoundError:
        print("❌ Ngrok não encontrado")
        print("   Baixe em: https://ngrok.com/download")
        print("   Adicione ao PATH do sistema")
    except Exception as e:
        print(f"❌ Erro ao iniciar ngrok: {e}")

if __name__ == "__main__":
    main()
