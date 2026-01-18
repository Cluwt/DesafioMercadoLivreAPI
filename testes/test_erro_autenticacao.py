#!/usr/bin/env python3
"""
Teste 1: Tratamento de Falhas de Autenticação
"""

import requests
import json
import sys
import os

# Adiciona pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_falha_autenticacao():
    """Testa falha de autenticação com token inválido"""
    print("🧪 Teste 1: Falha de Autenticação")
    print("=" * 50)
    
    # Testa com token inválido
    print("\n[1/3] Testando com token inválido...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=iphone&limit=5',
            headers={'Authorization': 'Bearer TOKEN_INVALIDO'},
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 401:
            print("✅ Erro 401 tratado corretamente")
            data = response.json()
            print(f"   Mensagem: {data.get('detail', 'Sem mensagem')}")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Testa sem token
    print("\n[2/3] Testando sem token...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=iphone&limit=5',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            print("✅ Requisição sem token funciona (endpoint público)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Testa API do ML com token expirado
    print("\n[3/3] Testando API ML com token expirado...")
    try:
        # Simula token expirado modificando .env temporariamente
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                content = f.read()
            
            # Backup e substitui token
            with open('.env.test', 'w') as f:
                f.write(content.replace(
                    os.getenv('ML_ACCESS_TOKEN', ''),
                    'TOKEN_EXPIRADO_12345'
                ))
            
            os.rename('.env', '.env.backup_test')
            os.rename('.env.test', '.env')
            
            # Tenta fazer busca
            response = requests.get(
                'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=celular&limit=3',
                timeout=20  # Aumentado para 20 segundos
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('erro'):
                    print("✅ Erro de autenticação tratado corretamente")
                    print(f"   Mensagem amigável: {data['erro']}")
                else:
                    print("⚠️ Busca funcionou (pode usar token cache)")
            else:
                print(f"❌ Status inesperado: {response.status_code}")
            
            # Restaura .env original
            if os.path.exists('.env.backup_test'):
                os.remove('.env')
                os.rename('.env.backup_test', '.env')
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        # Restaura .env em caso de erro
        if os.path.exists('.env.backup_test'):
            if os.path.exists('.env'):
                os.remove('.env')
            os.rename('.env.backup_test', '.env')
    
    print("\n🎯 Teste 1 concluído!")

if __name__ == "__main__":
    test_falha_autenticacao()
