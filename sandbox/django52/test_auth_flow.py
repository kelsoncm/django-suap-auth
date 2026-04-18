#!/usr/bin/env python
"""
Script para testar o fluxo completo de autenticação SUAP
Simula o que o Django faz durante a autenticação
"""
import os
import sys
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django_suap_auth.utils import get_oauth2_client, generate_state
import requests

print("=" * 80)
print("TESTE DE AUTENTICAÇÃO SUAP - SIMULAÇÃO DO FLUXO")
print("=" * 80)

print("\n1. PASSO 1: Gerar URL de Autorização")
print("-" * 80)
try:
    client = get_oauth2_client()
    state = generate_state()
    auth_url = client.get_authorization_url(state)
    print(f"✓ URL gerada com sucesso")
    print(f"  State: {state}")
    print(f"  URL: {auth_url}")
    print(f"\n  Próximo passo: Visite esta URL em seu navegador")
except Exception as e:
    print(f"✗ ERRO ao gerar URL: {e}")
    sys.exit(1)

print("\n2. PASSO 2: Verificar conectividade com SUAP")
print("-" * 80)
try:
    response = requests.get(
        f"{client.base_url}/o/authorize/",
        timeout=10,
        allow_redirects=False
    )
    print(f"✓ SUAP está acessível")
    print(f"  Status Code: {response.status_code}")
    print(f"  Headers: {dict(response.headers)}")
except requests.ConnectionError:
    print(f"✗ ERRO: Não foi possível conectar ao SUAP")
    print(f"  Verifique sua conexão com a internet")
    sys.exit(1)
except Exception as e:
    print(f"✗ ERRO: {e}")
    sys.exit(1)

print("\n3. PASSO 3: Verificar credenciais")
print("-" * 80)
if not settings.SUAP_CLIENT_ID:
    print("✗ ERRO: SUAP_CLIENT_ID não está configurado")
    sys.exit(1)
if not settings.SUAP_CLIENT_SECRET:
    print("✗ ERRO: SUAP_CLIENT_SECRET não está configurado")
    sys.exit(1)
print("✓ Credenciais configuradas")
print(f"  CLIENT_ID: {settings.SUAP_CLIENT_ID}")
print(f"  CLIENT_SECRET: {'*' * len(settings.SUAP_CLIENT_SECRET)}")

print("\n4. INSTRUÇÕES PARA COMPLETAR O TESTE")
print("-" * 80)
print("""
Para testar o fluxo completo de autenticação:

1. Abra o navegador e visite:
   http://localhost:8000/

2. Clique em "Entrar com o SUAP"

3. Na página de login, clique em "Entrar com o SUAP"

4. Você será redirecionado para: https://suap.ifrn.edu.br/o/authorize/
   
5. Faça login com suas credenciais SUAP

6. Autorize o acesso aos dados solicitados

7. Você será redirecionado de volta para:
   http://localhost:8000/auth/suap/callback/?code=XXX&state=YYY

8. O Django irá:
   - Validar o state
   - Trocar o código por um token de acesso
   - Buscar suas informações do SUAP
   - Criar/atualizar seu usuário no Django
   - Redirecionar para /dashboard/

Se algo falhar, você verá uma mensagem de erro na página.
""")

print("\n5. PROBLEMAS CONHECIDOS")
print("-" * 80)
print("""
• Credenciais expiradas/inválidas
  → Verifique SUAP_CLIENT_ID e SUAP_CLIENT_SECRET em .env

• "State Mismatch"
  → Limpe cookies do navegador e tente novamente

• Timeout ao conectar com SUAP
  → Verifique sua conexão com a internet

• Permissões insuficientes
  → Verifique se seu usuário SUAP tem acesso aos scopes solicitados

Para mais detalhes, veja: TROUBLESHOOTING_PT-BR.md
""")

print("=" * 80)
print("FIM DO TESTE")
print("=" * 80)

