# Configuração

## Configurações Obrigatórias

```python
SUAP_CLIENT_ID = "your-client-id"
SUAP_CLIENT_SECRET = "your-client-secret"
SUAP_REDIRECT_URI = "https://yourapp.example.com/auth/suap/callback/"
```

## Configurações Opcionais

| Configuração                 | Padrão                       | Descrição                                                                             |
|------------------------------|------------------------------|---------------------------------------------------------------------------------------|
| `SUAP_BASE_URL`              | `https://suap.ifrn.edu.br`   | URL base do SUAP                                                                      |
| `SUAP_AUTH_SCOPES`           | `["identificacao", "email"]` | Escopos OAuth2                                                                        |
| `SUAP_USER_LOOKUP_FIELD`     | `"username"`                 | Campo do usuário Django usado para busca                                              |
| `SUAP_USER_ATTR_MAP`         | Veja abaixo                  | Mapeamento de campos do modelo de usuário para chaves de resposta SUAP                |
| `SUAP_USER_JSON_FIELD`       | `None`                       | Campo para armazenar a resposta JSON completa do SUAP                                 |
| `SUAP_AUTH_DIRECT_REDIRECT`  | `True`                       | Redirecionar diretamente para SUAP (`True`) ou mostrar página intermediária (`False`) |

## Backend de Autenticação

```python
AUTHENTICATION_BACKENDS = [
    "django_suap_auth.backends.SuapAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```
