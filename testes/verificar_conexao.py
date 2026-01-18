#!/usr/bin/env python3
"""
Verifica se o servidor está online antes de rodar os testes
"""

import requests
import sys
import time

def verificar_conexao():
    """Verifica se o servidor está respondendo"""
    print("🔍 Verificando conexão com o servidor...")
    print("=" * 50)
    
    url = "https://chery-triazolic-walton.ngrok-free.dev"
    
    # Testa conexão básica
    try:
        print(f"\n[1/3] Testando conexão com {url}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Servidor respondeu!")
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        else:
            print(f"❌ Servidor respondeu com status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - servidor não respondeu em 10 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor offline ou URL incorreta")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    # Testa API de busca
    try:
        print(f"\n[2/3] Testando API de busca...")
        response = requests.get(f"{url}/api/buscar?q=teste&limit=1", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API de busca funcionando!")
            print(f"   Total de produtos: {data.get('total', 'N/A')}")
            if data.get('erro'):
                print(f"   Erro na API: {data['erro']}")
        else:
            print(f"❌ API respondeu com status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return False
    
    # Testa página HTML
    try:
        print(f"\n[3/3] Testando página HTML...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            if 'html' in response.headers.get('Content-Type', '').lower():
                print("✅ Página HTML funcionando!")
                print(f"   Tamanho: {len(response.text)} bytes")
            else:
                print("⚠️ Resposta não é HTML")
        else:
            print(f"❌ Página respondeu com status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na página: {e}")
        return False
    
    print("\n🎉 Todas as verificações passaram!")
    print("   Servidor está online e funcionando")
    return True

def main():
    if verificar_conexao():
        print("\n✅ Pode executar os testes agora!")
        print("\nExecute: RODAR_TODOS.bat")
    else:
        print("\n❌ Verifique:")
        print("   1. Se o servidor está rodando")
        print("   2. Se o ngrok está ativo")
        print("   3. Se a URL está correta")
        print("   4. Se há internet")

if __name__ == "__main__":
    main()
