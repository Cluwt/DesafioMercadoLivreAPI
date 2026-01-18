#!/usr/bin/env python3
"""
Teste 3: Mensagens Amigáveis ao Usuário
"""

import requests
import json
import sys
import os

# Adiciona pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_mensagens_amigaveis():
    """Testa se as mensagens de erro são amigáveis"""
    print("🧪 Teste 3: Mensagens Amigáveis ao Usuário")
    print("=" * 50)
    
    # Testa mensagem de erro genérica
    print("\n[1/3] Testando mensagem de erro genérica...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=produto_inexistente_xyz123&limit=5',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('erro'):
                erro_msg = data['erro']
                print(f"✅ Mensagem de erro: {erro_msg}")
                
                # Verifica se é amigável
                termos_tecnicos = ['Exception', 'Traceback', 'Error:', 'NoneType', 'KeyError']
                tem_termos_tecnicos = any(termo.lower() in erro_msg.lower() for termo in termos_tecnicos)
                
                if not tem_termos_tecnicos:
                    print("✅ Mensagem é amigável (sem termos técnicos)")
                else:
                    print("❌ Mensagem contém termos técnicos")
            else:
                print("⚠️ Sem mensagem de erro")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa mensagem de busca vazia
    print("\n[2/3] Testando mensagem de busca vazia...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=&limit=5',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('erro'):
                erro_msg = data['erro']
                print(f"✅ Mensagem: {erro_msg}")
                
                # Verifica se é construtiva
                if 'por favor' in erro_msg.lower() or 'tente' in erro_msg.lower():
                    print("✅ Mensagem é construtiva")
                else:
                    print("⚠️ Mensagem poderia ser mais construtiva")
            else:
                print("⚠️ Sem mensagem de erro")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa mensagem de limite excedido
    print("\n[3/3] Testando mensagem de limite excedido...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=celular&limit=100',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('erro'):
                erro_msg = data['erro']
                print(f"✅ Mensagem: {erro_msg}")
                
                # Verifica se explica o limite
                if 'limite' in erro_msg.lower() or 'máximo' in erro_msg.lower():
                    print("✅ Mensagem explica o limite")
                else:
                    print("⚠️ Mensagem não explica o limite")
            else:
                print("⚠️ Sem mensagem de erro (pode aceitar)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    print("\n🎯 Teste 3 concluído!")

if __name__ == "__main__":
    test_mensagens_amigaveis()
