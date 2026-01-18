#!/usr/bin/env python3
"""
Teste 2: Tratamento de Erros de Requisição à API
"""

import requests
import json
import sys
import os
import time

# Adiciona pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_erros_requisicao():
    """Testa tratamento de erros de requisição"""
    print("🧪 Teste 2: Erros de Requisição à API")
    print("=" * 50)
    
    # Testa timeout
    print("\n[1/4] Testando timeout...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=notebook&limit=5',
            timeout=0.001  # Timeout muito curto
        )
        print("⚠️ Requisição funcionou (pode ser muito rápida)")
    except requests.exceptions.Timeout:
        print("✅ Timeout tratado corretamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    # Testa conexão recusada
    print("\n[2/4] Testando conexão recusada...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=teste',  # URL inválida
            timeout=5
        )
        print("⚠️ Conexão funcionou (URL pode ser válida)")
    except requests.exceptions.ConnectionError:
        print("✅ Erro de conexão tratado corretamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    # Testa parâmetros inválidos
    print("\n[3/4] Testando parâmetros inválidos...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=&limit=1000',  # Parâmetros inválidos
            timeout=5
        )
        
        if response.status_code == 422:
            print("✅ Parâmetros inválidos tratados (422)")
            data = response.json()
            print(f"   Detalhes: {data}")
        elif response.status_code == 200:
            data = response.json()
            if data.get('erro'):
                print("✅ Erro tratado na resposta")
                print(f"   Mensagem: {data['erro']}")
            else:
                print("⚠️ Requisição aceita (validação pode ser no frontend)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Testa método não permitido
    print("\n[4/4] Testando método não permitido...")
    try:
        response = requests.post(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=teste',
            timeout=5
        )
        
        if response.status_code == 405:
            print("✅ Método não permitido tratado (405)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n🎯 Teste 2 concluído!")

if __name__ == "__main__":
    test_erros_requisicao()
