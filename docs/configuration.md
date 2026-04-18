# Configuração

## Configuração Básica

```python
# settings.py

SUAP_AUTH = {
    # Obrigatório
    'CLIENT_ID': 'your-client-id',
    'CLIENT_SECRET': 'your-client-secret',
    'REDIRECT_URI': 'https://yourapp.example.com/auth/suap/callback/',
    
    # Opcional
    'BASE_URL': 'https://suap.ifrn.edu.br',
    'SCOPES': ['identificacao', 'email'],
    'USER_LOOKUP_FIELD': 'username',
    'USER_ATTR_MAP': {
        'username': 'identificacao',
        'email': 'email_preferencial',
        ('first_name', 'last_name'): 'nome_usual',
    },
    'USER_JSON_FIELD': None,
    'DIRECT_REDIRECT': True,
}

AUTHENTICATION_BACKENDS = [
    'django_suap_auth.backends.SuapAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

## Campos Disponíveis

| Campo | Obrigatório | Padrão | Descrição |
|-------|------------|--------|-----------|
| `CLIENT_ID` | ✅ | - | ID da aplicação OAuth2 no SUAP |
| `CLIENT_SECRET` | ✅ | - | Senha da aplicação OAuth2 no SUAP |
| `REDIRECT_URI` | ✅ | - | URL de callback (deve terminar com `/`) |
| `BASE_URL` | ❌ | `https://suap.ifrn.edu.br` | URL base do servidor SUAP |
| `SCOPES` | ❌ | `['identificacao', 'email']` | Lista de escopos OAuth2 solicitados |
| `USER_LOOKUP_FIELD` | ❌ | `'username'` | Campo do usuário Django usado para busca |
| `USER_ATTR_MAP` | ❌ | Veja abaixo | Mapeamento: Django → SUAP |
| `USER_JSON_FIELD` | ❌ | `None` | Campo para armazenar resposta JSON completa |
| `DIRECT_REDIRECT` | ❌ | `True` | Redireciona direto para SUAP ou mostra intermediária |

## Mapeamento de Atributos (USER_ATTR_MAP)

O dicionário `USER_ATTR_MAP` mapeia campos do modelo User do Django para chaves na resposta do SUAP:

```python
SUAP_AUTH = {
    # ...
    'USER_ATTR_MAP': {
        'username': 'identificacao',           # Campo simples
        'email': 'email_preferencial',
        'first_name': 'primeiro_nome',
        'last_name': 'ultimo_nome',
        ('first_name', 'last_name'): 'nome_usual',  # Múltiplos campos
    },
}
```

## Usando Variáveis de Ambiente

```python
import os
from pathlib import Path

SUAP_AUTH = {
    'CLIENT_ID': os.getenv('SUAP_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('SUAP_CLIENT_SECRET'),
    'REDIRECT_URI': os.getenv('SUAP_REDIRECT_URI'),
    'BASE_URL': os.getenv('SUAP_BASE_URL', 'https://suap.ifrn.edu.br'),
    'SCOPES': os.getenv('SUAP_SCOPES', 'identificacao,email').split(','),
    'DIRECT_REDIRECT': os.getenv('SUAP_DIRECT_REDIRECT', 'True') == 'True',
}
```

## Arquivo .env Exemplo

```env
SUAP_CLIENT_ID=your-client-id
SUAP_CLIENT_SECRET=your-client-secret
SUAP_REDIRECT_URI=http://localhost:8000/auth/suap/callback/
SUAP_BASE_URL=https://suap.ifrn.edu.br
SUAP_SCOPES=identificacao,email
SUAP_DIRECT_REDIRECT=False
```
