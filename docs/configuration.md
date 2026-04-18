# Configuração

## Configuração Básica

Todas as opções ficam em um único dicionário `SUAP_AUTH` no `settings.py`:

```python
# settings.py

SUAP_AUTH = {
    # --- Obrigatório ---
    'CLIENT_ID': 'your-client-id',
    'CLIENT_SECRET': 'your-client-secret',
    'REDIRECT_URI': 'https://yourapp.example.com/auth/suap/callback/',

    # --- Conexão (opcional) ---
    'BASE_URL': 'https://suap.ifrn.edu.br',       # padrão
    'SCOPES': ['identificacao', 'email'],           # padrão

    # --- Mapeamento de usuário (opcional) ---
    'USER_LOOKUP_FIELD': 'username',                # padrão
    'USER_ATTR_MAP': {                              # padrão
        'username': 'identificacao',
        'email': 'email',
        ('first_name', 'last_name'): 'nome_usual',
    },
    'USER_JSON_FIELD': None,                        # padrão

    # --- Criação e atualização de usuários (opcional) ---
    'CREATE_USER': True,                            # padrão
    'USER_DEFAULTS': {'is_active': True},           # padrão
    'FIRST_USER_DEFAULTS': None,                    # padrão
    'UPDATE_FIELDS_ON_CREATE': None,                # padrão (todos os campos mapeados)
    'UPDATE_FIELDS_ON_LOGIN': None,                 # padrão (todos os campos mapeados)

    # --- Fluxo de login (opcional) ---
    'DIRECT_REDIRECT': True,                        # padrão
    'BACKEND': 'django_suap_auth.backends.SuapAuthBackend',  # padrão
}

AUTHENTICATION_BACKENDS = [
    'django_suap_auth.backends.SuapAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

---

## Referência de Settings

### Conexão

| Setting | Obrigatório | Padrão | Descrição |
|---------|-------------|--------|-----------|
| `CLIENT_ID` | ✅ | — | ID da aplicação OAuth2 registrada no SUAP |
| `CLIENT_SECRET` | ✅ | — | Chave secreta da aplicação OAuth2 |
| `REDIRECT_URI` | ✅ | — | URL de callback cadastrada no SUAP (deve terminar com `/`) |
| `BASE_URL` | ❌ | `'https://suap.ifrn.edu.br'` | URL base do servidor SUAP |
| `SCOPES` | ❌ | `['identificacao', 'email']` | Escopos OAuth2 solicitados na autorização |

### Mapeamento de Usuário

| Setting | Obrigatório | Padrão | Descrição |
|---------|-------------|--------|-----------|
| `USER_LOOKUP_FIELD` | ❌ | `'username'` | Campo do model `User` usado para localizar o usuário |
| `USER_ATTR_MAP` | ❌ | Veja [Mapeamento de Atributos](attribute-mapping.md) | Dicionário `campo_django → chave_suap` |
| `USER_JSON_FIELD` | ❌ | `None` | Se definido, armazena o JSON completo do SUAP neste campo |

### Criação e Atualização de Usuários

| Setting | Obrigatório | Padrão | Descrição |
|---------|-------------|--------|-----------|
| `CREATE_USER` | ❌ | `True` | Quando `False`, nega o login de usuários sem conta local (lança `SuapUserNotAllowedError`) |
| `USER_DEFAULTS` | ❌ | `{'is_active': True}` | Campos aplicados ao **criar** um usuário. Também são reaplicados a cada login (ex.: reactivar conta inativa) |
| `FIRST_USER_DEFAULTS` | ❌ | `None` | Quando definido, substitui `USER_DEFAULTS` somente para o **primeiro usuário** criado no banco. Útil para promover automaticamente o primeiro cadastro a superusuário |
| `UPDATE_FIELDS_ON_CREATE` | ❌ | `None` | Lista de campos mapeados gravados na criação. `None` = todos; `[]` = nenhum |
| `UPDATE_FIELDS_ON_LOGIN` | ❌ | `None` | Lista de campos mapeados sincronizados a cada login. `None` = todos; `[]` = nenhum |

### Fluxo de Login

| Setting | Obrigatório | Padrão | Descrição |
|---------|-------------|--------|-----------|
| `DIRECT_REDIRECT` | ❌ | `True` | `True` redireciona imediatamente ao SUAP; `False` exibe uma página intermediária de confirmação |
| `BACKEND` | ❌ | `'django_suap_auth.backends.SuapAuthBackend'` | Caminho Python do backend de autenticação usado em `login()` |

---

## Exemplos de Configuração

### Negar criação automática de usuários

Útil quando os usuários devem ser pré-cadastrados por um administrador:

```python
SUAP_AUTH = {
    # ...
    'CREATE_USER': False,
}
```

Usuários sem conta local receberão uma mensagem de erro e serão redirecionados ao `LOGIN_URL`.

### Promover o primeiro usuário a superusuário

```python
SUAP_AUTH = {
    # ...
    'USER_DEFAULTS': {'is_active': True, 'is_superuser': False, 'is_staff': False},
    'FIRST_USER_DEFAULTS': {'is_active': True, 'is_superuser': True, 'is_staff': True},
}
```

O primeiro usuário a se autenticar será superusuário; os demais serão usuários comuns.

### Sincronizar apenas alguns campos a cada login

```python
SUAP_AUTH = {
    # ...
    'UPDATE_FIELDS_ON_LOGIN': ['email', 'first_name', 'last_name'],
}
```

### Congelar os dados do usuário após a criação

Cria o usuário com todos os dados do SUAP, mas nunca os sobrescreve nos logins seguintes:

```python
SUAP_AUTH = {
    # ...
    'UPDATE_FIELDS_ON_CREATE': None,  # todos os campos na criação
    'UPDATE_FIELDS_ON_LOGIN': [],     # nenhum campo nos logins seguintes
}
```

### Página de login intermediária

Ao invés de redirecionar automaticamente ao SUAP:

```python
SUAP_AUTH = {
    # ...
    'DIRECT_REDIRECT': False,
}
```

Veja [Personalizando o login.html](#personalizando-o-loginhtml) para customizar a página exibida.

---

## Personalizando o login.html

Quando `DIRECT_REDIRECT = False`, a view exibe o template `django_suap_auth/login.html`.

### Sobrescrever o template padrão

Crie o arquivo `templates/django_suap_auth/login.html` no seu projeto (certifique-se de que `APP_DIRS = True` ou que o diretório esteja em `DIRS`):

```html
{% extends "base.html" %}

{% block content %}
  <h1>Entrar</h1>
  <p>Use sua conta SUAP para acessar o sistema.</p>
  <form method="post">
    {% csrf_token %}
    <button type="submit">Entrar com SUAP</button>
  </form>
{% endblock %}
```

O template padrão é um HTML mínimo sem dependências — substitua-o livremente.

### Usar um template diferente via subclasse

Subclasse `SuapLoginView` e defina `intermediate_template`:

```python
# myapp/views.py
from django_suap_auth.views import SuapLoginView

class MyLoginView(SuapLoginView):
    intermediate_template = "myapp/custom_login.html"
```

```python
# myapp/urls.py
from .views import MyLoginView

urlpatterns = [
    path('auth/suap/login/', MyLoginView.as_view(), name='suap-login'),
    # ...
]
```

---

## Usando Variáveis de Ambiente

```python
import os

SUAP_AUTH = {
    'CLIENT_ID': os.getenv('SUAP_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('SUAP_CLIENT_SECRET'),
    'REDIRECT_URI': os.getenv('SUAP_REDIRECT_URI'),
    'BASE_URL': os.getenv('SUAP_BASE_URL', 'https://suap.ifrn.edu.br'),
    'SCOPES': os.getenv('SUAP_SCOPES', 'identificacao,email').split(','),
    'DIRECT_REDIRECT': os.getenv('SUAP_DIRECT_REDIRECT', 'True') == 'True',
    'CREATE_USER': os.getenv('SUAP_CREATE_USER', 'True') == 'True',
}
```

### Arquivo `.env` de exemplo

```env
SUAP_CLIENT_ID=your-client-id
SUAP_CLIENT_SECRET=your-client-secret
SUAP_REDIRECT_URI=http://localhost:8000/auth/suap/callback/
SUAP_BASE_URL=https://suap.ifrn.edu.br
SUAP_SCOPES=identificacao,email
SUAP_DIRECT_REDIRECT=False
SUAP_CREATE_USER=True
```
