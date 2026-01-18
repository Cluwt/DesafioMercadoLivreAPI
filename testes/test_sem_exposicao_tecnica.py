#!/usr/bin/env python3
"""
Teste 4: Sem Exposição de Erros Técnicos ou Stack Traces
"""

import requests
import json
import sys
import os
import re

# Adiciona pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_sem_exposicao_tecnica():
    """Testa se não expõe erros técnicos na interface"""
    print("🧪 Teste 4: Sem Exposição de Erros Técnicos")
    print("=" * 50)
    
    # Lista de termos técnicos que não devem aparecer
    termos_proibidos = [
        'Traceback', 'Exception', 'Error:', 'NoneType', 
        'KeyError', 'ValueError', 'AttributeError',
        'File "', 'line ', 'in ', 'python',
        'uvicorn', 'fastapi', 'requests',
        'mercadolibre.com', 'api.mercadolibre',
        'ML_CLIENT_ID', 'ML_CLIENT_SECRET'
    ]
    
    # Testa resposta JSON da API
    print("\n[1/3] Verificando respostas JSON...")
    try:
        # Força erro com parâmetro inválido
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=teste&limit=abc',
            timeout=5
        )
        
        resposta_texto = response.text
        print(f"Status: {response.status_code}")
        print(f"Resposta: {resposta_texto[:200]}...")
        
        # Verifica termos proibidos
        termos_encontrados = []
        for termo in termos_proibidos:
            if termo.lower() in resposta_texto.lower():
                termos_encontrados.append(termo)
        
        if not termos_encontrados:
            print("✅ Nenhum termo técnico encontrado na resposta")
        else:
            print(f"❌ Termos técnicos encontrados: {termos_encontrados}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa página HTML (interface)
    print("\n[2/3] Verificando página HTML...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/',
            timeout=5
        )
        
        if response.status_code == 200:
            html_content = response.text
            
            # Verifica se não há stack traces no HTML
            stack_trace_patterns = [
                r'Traceback \(most recent call last\):',
                r'File ".*", line \d+',
                r'\w*Error:.*',
                r'at .*\.py.*line \d+'
            ]
            
            stack_encontrado = False
            for pattern in stack_trace_patterns:
                if re.search(pattern, html_content, re.IGNORECASE):
                    print(f"❌ Stack trace encontrado: {pattern}")
                    stack_encontrado = True
                    break
            
            if not stack_encontrado:
                print("✅ Nenhum stack trace encontrado no HTML")
            else:
                print("❌ Stack trace exposto na interface")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    # Testa headers de resposta
    print("\n[3/3] Verificando headers de resposta...")
    try:
        response = requests.get(
            'https://chery-triazolic-walton.ngrok-free.dev/api/buscar?q=erro_forcado',
            timeout=5
        )
        
        # Verifica headers que podem expor informações
        headers_perigosos = ['Server', 'X-Powered-By', 'X-Debug']
        
        for header in headers_perigosos:
            if header in response.headers:
                print(f"⚠️ Header potencialmente perigoso: {header}={response.headers[header]}")
            else:
                print(f"✅ Header seguro: {header} não exposto")
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    print("\n🎯 Teste 4 concluído!")

if __name__ == "__main__":
    test_sem_exposicao_tecnica()
