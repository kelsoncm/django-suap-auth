# 🔍 Guia de Diagnóstico - Falha de Autenticação SUAP

## 📊 Seu Problema

Você relata que o fluxo de autenticação:
1. ✅ Vai até o SUAP corretamente
2. ✅ Retorna do SUAP com `code` e `state`
3. ❌ Mas então volta para `/auth/suap/login/` (página de login)

**Isso significa**: A função `authenticate()` está retornando `None`, ou seja, o usuário não está sendo criado/autenticado no Django.

## ✨ Melhorias Implementadas

### 1. **Logging Detalhado** 
- Arquivo: `django_suap_auth/views.py`
- Cada etapa do callback agora registra o que está acontecendo
- Inclui informações sobre qual etapa falhou

### 2. **View de Debug**
- URL: `/auth/suap/debug/`
- Retorna informações em JSON sobre:
  - Status de autenticação
  - Dados da sessão
  - Configurações do SUAP
  - Parametros da requisição

### 3. **Documentação Detalhada**
- `DIAGNOSTIC_PT-BR.md` - Guia completo de diagnóstico

## 🚀 Como Diagnosticar (Passo a Passo)

### TERMINAL 1: Iniciar o Servidor

```bash
cd sandbox/django52
python manage.py runserver
```

**Deixe rodando** - você verá os logs aqui

### TERMINAL 2: Fazer Login

1. Abra navegador (incógnito/novo perfil)
2. Visite: `http://localhost:8000/dashboard/`
3. Clique em "Entrar com SUAP"
4. Clique em "Entrar com SUAP" (na página intermediária)
5. Faça login no SUAP
6. Autorize o acesso
7. **Observe o TERMINAL 1**

### OBSERVAR OS LOGS

No TERMINAL 1, você verá:

```
================================================================================
SUAP CALLBACK - Iniciando fluxo de autenticação
Request path: /auth/suap/callback/
Query string: <QueryDict: {'code': ['...'], 'state': ['...']}>
Session ID: xxxxxx
--------------------------------------------------------------------------------
1. Validando State (CSRF)
   State recebido: R1deG3LmL5bYkq...
   State armazenado: R1deG3LmL5bYkq...
   ✓ State validado com sucesso
--------------------------------------------------------------------------------
2. Trocando código por token de acesso
   Code recebido: abc123def456...
   ✓ Token obtido com sucesso
   Token data keys: ['access_token', 'token_type', 'expires_in']
   Access token: eyJhbGciOiJIUzI1NiIsI...
--------------------------------------------------------------------------------
3. Buscando informações do usuário no SUAP
   ✓ Informações obtidas com sucesso
   User info keys: ['matricula', 'nome_usual', 'email', ...]
   User info: {'matricula': '12345678', 'nome_usual': 'João Silva', 'email': 'joao@ifrn.edu.br', ...}
--------------------------------------------------------------------------------
4. Autenticando usuário no Django
   ✓ Usuário autenticado: 12345678
   ✓ Usuário logado na sessão
--------------------------------------------------------------------------------
5. Redirecionando usuário
   Next URL: /dashboard/
   ✓ Redirecionando para: /dashboard/
================================================================================
```

## 🔴 Se Ver Erro

### Erro no Passo 1: "✗ ERRO: State mismatch!"

**Causa**: Problema de sessão/cookies
**Solução**: 
- Limpe cookies do navegador (F12 → Application → Cookies)
- Tente em navegador incógnito
- Pode ser problema de CSRF token expirado

### Erro no Passo 2: "✗ ERRO ao obter token"

**Causa**: Problema com o código autorizado ou credenciais SUAP
**Solução**:
- Verifique se SUAP_CLIENT_SECRET está correto em `.env`
- Reinicie o servidor
- O `code` pode ter expirado (válido por pouco tempo)

### Erro no Passo 3: "✗ ERRO ao obter informações"

**Causa**: Token de acesso inválido ou scopes insuficientes
**Solução**:
- Verifique se os scopes em `SUAP_AUTH_SCOPES` você tem acesso
- Verifique se sua conta SUAP não está bloqueada
- Contate suporte do SUAP se persistir

### Erro no Passo 4: "✗ ERRO: authenticate() retornou None"

**Causa**: Uma das possibilidades:
1. Os campos do SUAP não coincidem com o mapeamento esperado
2. Backend SUAP não está ativado
3. Campo `matricula` (username) não está sendo retornado pelo SUAP

**Solução**:

a) **Verifique o backend**:
   Abra `sandbox/django52/config/settings.py` e confirme:
   ```python
   AUTHENTICATION_BACKENDS = [
       "django_suap_auth.backends.SuapAuthBackend",  # ← Deve estar aqui!
       "django.contrib.auth.backends.ModelBackend",
   ]
   ```

b) **Verifique o mapeamento**:
   Nos logs, você verá "User info:" com todos os campos retornados pelo SUAP.
   
   Em `django_suap_auth/utils.py`, veja `DEFAULT_USER_ATTR_MAP`:
   ```python
   DEFAULT_USER_ATTR_MAP = {
       "username": "matricula",  # Deve existir em user_info
       "email": "email",
       ("first_name", "last_name"): "nome_usual",
   }
   ```
   
   Se o SUAP não retorna `matricula`, customize em `settings.py`:
   ```python
   SUAP_USER_ATTR_MAP = {
       "username": "outro_campo",  # Campo que identifica o usuário
       "email": "email",
   }
   ```

c) **Teste qual campo usar**:
   Veja exatamente quais campos o SUAP retorna nos logs (passo 3).
   Use um desses campos para `username`.

## 🔗 URLs Úteis para Debug

- `http://localhost:8000/` - Home page
- `http://localhost:8000/dashboard/` - Dashboard (protegido)
- `http://localhost:8000/auth/suap/login/` - Página de login
- `http://localhost:8000/auth/suap/debug/` - Informações de debug (JSON)

## 📋 Checklist

Antes de fazer login, verifique:

- [ ] `.env` tem credenciais corretas (reinicie servidor se alterou)
- [ ] `AUTHENTICATION_BACKENDS` tem `django_suap_auth.backends.SuapAuthBackend`
- [ ] Usando navegador incógnito ou sem cookies
- [ ] Terminal do servidor está rodando e mostrando logs
- [ ] Você tem acesso ativo ao SUAP

## 🆘 Se Ainda Não Funcionar

1. **Copie os logs completos** do console
2. **Compartilhe os logs** comigo
3. **Especifique qual erro** você vê:
   - State mismatch?
   - Token error?
   - Authentication failed?
   - Outro?

Com os logs, poderei diagnosticar exatamente o problema.

## 💡 Dica Importante

O erro "Authentication failed" provavelmente é porque:
- O campo `matricula` não está sendo retornado pelo SUAP
- Ou está com nome diferente (ex: `user_id`, `cpf`, etc.)

**Solução**: Customize `SUAP_USER_ATTR_MAP` com o campo correto.

## 🎯 Próximos Passos

1. Reinicie o servidor: `python manage.py runserver`
2. Faça login observando os logs
3. Compartilhe os logs comigo
4. Vamos identificar e corrigir juntos!


