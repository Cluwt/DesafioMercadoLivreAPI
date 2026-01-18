#!/usr/bin/env python3
"""
Teste 5: Interface de Tratamento de Erros
"""

import requests
import json
import sys
import os
import time

# Adiciona pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_interface_erros():
    """Testa como a interface lida com erros"""
    print("🧪 Teste 5: Interface de Tratamento de Erros")
    print("=" * 50)
    
    # Testa busca sem resultados
    print("\n[1/4] Testando busca sem resultados...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=produto_inexistente_xyz123456&limit=5',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('total', 0) == 0 and not data.get('erro'):
                print("✅ Busca vazia tratada corretamente (total=0)")
            elif data.get('erro'):
                print(f"✅ Erro tratado: {data['erro']}")
            else:
                print("⚠️ Resposta inesperada")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa caracteres especiais
    print("\n[2/4] Testando caracteres especiais...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=teste@#$%&limit=5',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Caracteres especiais aceitos")
            
            if data.get('erro'):
                print(f"   Erro: {data['erro']}")
            else:
                print(f"   Resultados: {data.get('total', 0)} produtos")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa termo muito longo
    print("\n[3/4] Testando termo muito longo...")
    try:
        termo_longo = "a" * 1000  # 1000 caracteres
        response = requests.get(
            f'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q={termo_longo}&limit=5',
            timeout=15  # Aumentado para 15 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('erro'):
                print(f"✅ Termo longo tratado: {data['erro'][:100]}...")
            else:
                print("⚠️ Termo longo aceito (pode ter limite maior)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa múltiplas requisições simultâneas
    print("\n[4/4] Testando múltiplas requisições...")
    try:
        import threading
        
        resultados = []
        
        def fazer_requisicao(termo):
            try:
                response = requests.get(
                    f'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q={termo}&limit=3',
                    timeout=20  # Aumentado para 20 segundos
                )
                resultados.append({
                    'termo': termo,
                    'status': response.status_code,
                    'data': response.json() if response.status_code == 200 else None
                })
            except Exception as e:
                resultados.append({
                    'termo': termo,
                    'erro': str(e)
                })
        
        # Dispara múltiplas requisições
        termos = ['celular', 'notebook', 'tablet', 'tv', 'fone']
        threads = []
        
        for termo in termos:
            thread = threading.Thread(target=fazer_requisicao, args=(termo,))
            threads.append(thread)
            thread.start()
        
        # Aguarda todas terminarem
        for thread in threads:
            thread.join()
        
        # Verifica resultados
        sucessos = sum(1 for r in resultados if 'status' in r and r['status'] == 200)
        erros = sum(1 for r in resultados if 'erro' in r or ('status' in r and r['status'] != 200))
        
        print(f"✅ Requisições simultâneas: {sucessos} sucessos, {erros} erros")
        
        for resultado in resultados:
            if 'erro' in resultado:
                print(f"   ❌ Erro em {resultado['termo']}: {resultado['erro']}")
            elif resultado['status'] != 200:
                print(f"   ❌ Status {resultado['status']} em {resultado['termo']}")
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    print("\n🎯 Teste 5 concluído!")

if __name__ == "__main__":
    test_interface_erros()
