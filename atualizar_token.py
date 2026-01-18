
"""
Atualiza tokens do Mercado Livre quando expirados
"""

import os
import json
import requests
import urllib.parse
import webbrowser

def trocar_codigo_por_token(code):
    """Troca código por tokens diretamente na API do ML"""
    
    # Lê credenciais do .env
    client_id = None
    client_secret = None
    redirect_uri = "https://chery-triazolic-walton.ngrok-free.dev/"
    
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ML_CLIENT_ID='):
                    client_id = line.split('=')[1].strip()
                elif line.startswith('ML_CLIENT_SECRET='):
                    client_secret = line.split('=')[1].strip()
    
    if not client_id or not client_secret:
        print("❌ Credenciais não encontradas no .env")
        return None, None
    
    # Faz requisição direta para API do ML
    token_url = "https://api.mercadolibre.com/oauth/token"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }
    
    try:
        response = requests.post(token_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token'), data.get('refresh_token')
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None, None

def atualizar_env(access_token, refresh_token):
    """Atualiza .env"""
    if os.path.exists('.env'):
        if os.path.exists('.env.backup'):
            os.remove('.env.backup')
        os.rename('.env', '.env.backup')
        print("✅ Backup criado")
    
    lines = []
    if os.path.exists('.env.backup'):
        with open('.env.backup', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    new_lines = []
    has_access = has_refresh = False
    
    for line in lines:
        if line.startswith('ML_ACCESS_TOKEN='):
            new_lines.append(f'ML_ACCESS_TOKEN={access_token}\n')
            has_access = True
        elif line.startswith('ML_REFRESH_TOKEN='):
            new_lines.append(f'ML_REFRESH_TOKEN={refresh_token}\n')
            has_refresh = True
        else:
            new_lines.append(line)
    
    if not has_access:
        new_lines.append(f'ML_ACCESS_TOKEN={access_token}\n')
    if not has_refresh:
        new_lines.append(f'ML_REFRESH_TOKEN={refresh_token}\n')
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ .env atualizado!")

def main():
    print("🔄 Atualizar Tokens")
    print("=" * 25)
    
    # 1. Gera URL e abre navegador
    print("\n[1/2] Abrindo página de autorização...")
    
    # Lê credenciais do .env
    client_id = None
    redirect_uri = "https://chery-triazolic-walton.ngrok-free.dev/"
    
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ML_CLIENT_ID='):
                    client_id = line.split('=')[1].strip()
    
    if not client_id:
        print("❌ ML_CLIENT_ID não encontrado no .env")
        return
    
    # Gera URL de autorização
    auth_url = (
        f"https://auth.mercadolivre.com.br/authorization"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
    )
    
    print("✅ Abrindo navegador...")
    print("   Autorize a aplicação")
    webbrowser.open(auth_url)
    
    # 2. Pega código da URL
    print("\n[2/2] Cole o código da URL abaixo:")
    print("   Após autorizar, copie a URL do navegador")
    print("   Ex: https://chery-triazolic-walton.ngrok-free.dev/?code=TG-XXXXX")
    print("   Ou cole só o código: TG-XXXXX")
    
    url_input = input("URL ou código: ").strip()
    
    # Extrai código da URL ou usa direto
    if "?code=" in url_input:
        parsed_url = urllib.parse.urlparse(url_input)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        auth_code = query_params.get('code', [None])[0]
    else:
        auth_code = url_input
    
    if not auth_code:
        print("❌ Código não fornecido")
        return
    
    print(f"✅ Código capturado: {auth_code[:30]}...")
    
    # 3. Troca código por tokens
    print("\n🔄 Obtendo novos tokens...")
    access, refresh = trocar_codigo_por_token(auth_code)
    
    if not access:
        print("❌ Falha ao obter tokens")
        return
    
    print("✅ Tokens obtidos")
    
    # 4. Atualiza .env
    print("\n📝 Atualizando .env...")
    atualizar_env(access, refresh)
    
    print("\n🎉 Tokens atualizados com sucesso!")

if __name__ == "__main__":
    main()
