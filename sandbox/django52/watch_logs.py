rom #!/usr/bin/env python
"""
Script para capturar e exibir logs de autenticação SUAP
Útil para troubleshooting
"""
import os
import sys
import logging
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

print("=" * 80)
print("CAPTURADOR DE LOGS - AUTENTICAÇÃO SUAP")
print("=" * 80)
print()
print("Este script configura logging detalhado para o django-suap-auth.")
print()
print("INSTRUÇÕES:")
print("1. Abra outro terminal e execute: python manage.py runserver")
print("2. Em um navegador, acesse: http://localhost:8000/dashboard/")
print("3. Complete o fluxo de login (clique em 'Entrar com SUAP')")
print("4. Faça login no SUAP")
print("5. Os logs abaixo mostrarão exatamente o que está acontecendo")
print()
print("=" * 80)
print("LOGS EM TEMPO REAL")
print("=" * 80)
print()

# Configurar logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

# Obter loggers
logger_suap = logging.getLogger('django_suap_auth')
logger_django = logging.getLogger('django')

# Mostrar informações de configuração
from django.conf import settings
from django_suap_auth.utils import get_suap_settings

print("CONFIGURAÇÃO ATUAL:")
suap_auth = getattr(settings, 'SUAP_AUTH', {})
print(f"  SUAP_AUTH CLIENT_ID: {str(suap_auth.get('CLIENT_ID', ''))[:20]}...")
print(f"  SUAP_AUTH DIRECT_REDIRECT: {suap_auth.get('DIRECT_REDIRECT', 'NÃO DEFINIDO')}")
print(f"  LOGIN_URL: {settings.LOGIN_URL}")
print(f"  LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
print(f"  AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
print()

# Simular um teste de callback (apenas informação)
print("ESTRUTURA DE LOGS A ESPERAR:")
print("""
Ao fazer login, você verá:

[django_suap_auth] INFO: ================================================================================
[django_suap_auth] INFO: SUAP CALLBACK - Iniciando fluxo de autenticação
[django_suap_auth] INFO: Request path: /auth/suap/callback/
[django_suap_auth] INFO: Query string: <QueryDict: {'code': [...], 'state': [...]}>
[django_suap_auth] INFO: Session ID: xxxxxx

[django_suap_auth] INFO: 1. Validando State (CSRF)
[django_suap_auth] INFO:    ✓ State validado com sucesso

[django_suap_auth] INFO: 2. Trocando código por token de acesso
[django_suap_auth] INFO:    ✓ Token obtido com sucesso

[django_suap_auth] INFO: 3. Buscando informações do usuário no SUAP
[django_suap_auth] INFO:    ✓ Informações obtidas com sucesso
[django_suap_auth] INFO:    User info: {...}

[django_suap_auth] INFO: 4. Autenticando usuário no Django
[django_suap_auth] INFO:    ✓ Usuário autenticado: username
[django_suap_auth] INFO:    ✓ Usuário logado na sessão

[django_suap_auth] INFO: 5. Redirecionando usuário
[django_suap_auth] INFO:    ✓ Redirecionando para: /dashboard/
""")

print()
print("Se houver erro, você verá mensagens com ✗ indicando onde falhou.")
print()
print("Iniciando servidor com logging detalhado...")
print("Pressione CTRL+C para parar.")
print()

# Manter o script rodando
try:
    while True:
        pass
except KeyboardInterrupt:
    print()
    print("=" * 80)
    print("Logging finalizado.")
    print("=" * 80)

