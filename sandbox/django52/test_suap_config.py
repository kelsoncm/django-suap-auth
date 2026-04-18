#!/usr/bin/env python
"""
Script para testar a configuração do SUAP no sandbox Django 5.2
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django_suap_auth.utils import get_suap_settings, get_oauth2_client

print("=" * 80)
print("TESTE DE CONFIGURAÇÃO SUAP - DJANGO 5.2 SANDBOX")
print("=" * 80)

print("\n1. Variáveis de Ambiente:")
print(f"   SUAP_CLIENT_ID: {os.environ.get('SUAP_CLIENT_ID', 'NÃO DEFINIDO')}")
print(f"   SUAP_CLIENT_SECRET: {os.environ.get('SUAP_CLIENT_SECRET', 'NÃO DEFINIDO')[:20]}...")
print(f"   SUAP_REDIRECT_URI: {os.environ.get('SUAP_REDIRECT_URI', 'NÃO DEFINIDO')}")
print(f"   SUAP_DIRECT_REDIRECT: {os.environ.get('SUAP_DIRECT_REDIRECT', 'NÃO DEFINIDO')}")

print("\n2. Configurações Django:")
suap_auth = getattr(settings, 'SUAP_AUTH', {})
print(f"   SUAP_AUTH CLIENT_ID: {suap_auth.get('CLIENT_ID', 'NÃO DEFINIDO')}")
print(f"   SUAP_AUTH CLIENT_SECRET: {str(suap_auth.get('CLIENT_SECRET', 'NÃO DEFINIDO'))[:20]}...")
print(f"   SUAP_AUTH REDIRECT_URI: {suap_auth.get('REDIRECT_URI', 'NÃO DEFINIDO')}")
print(f"   SUAP_AUTH DIRECT_REDIRECT: {suap_auth.get('DIRECT_REDIRECT', 'NÃO DEFINIDO')}")
print(f"   LOGIN_URL: {settings.LOGIN_URL}")
print(f"   LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")

print("\n3. Configurações SUAP internas:")
try:
    cfg = get_suap_settings()
    for key, value in cfg.items():
        if key == 'client_secret':
            value = value[:20] + "..."
        print(f"   {key}: {value}")
except Exception as e:
    print(f"   ERRO: {e}")

print("\n4. OAuth2 Client:")
try:
    client = get_oauth2_client()
    print(f"   client_id: {client.client_id}")
    print(f"   redirect_uri: {client.redirect_uri}")
    print(f"   scopes: {client.scopes}")
    print(f"   base_url: {client.base_url}")

    # Teste de URL de autorização
    state = "test_state_123"
    auth_url = client.get_authorization_url(state)
    print(f"\n   URL de Autorização de teste:")
    print(f"   {auth_url}")
except Exception as e:
    print(f"   ERRO: {e}")

print("\n" + "=" * 80)
print("FIM DO TESTE")
print("=" * 80)

