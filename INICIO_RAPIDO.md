# ⚡ INÍCIO RÁPIDO - Diagnosticar Erro de Autenticação

## 🎯 Seu Problema em Uma Frase

Você consegue chegar até o SUAP, mas após retornar, o Django não cria o usuário (volta para login).

## ✅ Solução Rápida (5 minutos)

### 1️⃣ Terminal 1: Iniciar servidor
```bash
cd C:\Users\kelson\projetos\PESSOAL\django-suap-auth\sandbox\django52
python manage.py runserver
```

**Deixe este terminal aberto e observando**

### 2️⃣ Terminal 2: Fazer login
```bash
# Não execute nada aqui, apenas use o navegador
```

1. Abra navegador **INCÓGNITO** (importante!)
2. Visite: `http://localhost:8000/dashboard/`
3. Clique em **"Entrar com SUAP"**
4. Clique em **"Entrar com SUAP"** novamente
5. Faça login no SUAP
6. **Volte ao TERMINAL 1 e procure por:**

```
User info keys: [...]
User info: {...}
```

### 3️⃣ Analisar Resultado

#### ✅ Se vir "matricula" nos dados
```
User info keys: ['matricula', 'nome_usual', 'email', ...]
User info: {'matricula': '12345678', ...}
```
→ **Problema pode estar na configuração Django**

#### ❌ Se NÃO vir "matricula"
```
User info keys: ['user_id', 'name', 'email', ...]
```
→ **O campo de ID tem outro nome! Procure qual é**

#### ❌ Se vir erro na etapa 4
```
✗ ERRO: authenticate() retornou None
```
→ **Field mismatch - configuração de mapeamento errada**

## 🔧 Corrigir (Se Necessário)

### Se "matricula" virou "user_id"

Abra `C:\Users\kelson\projetos\PESSOAL\django-suap-auth\sandbox\django52\config\settings.py`

Procure por (ou adicione):
```python
SUAP_USER_ATTR_MAP = {
    'username': 'user_id',  # ← Altere para o campo correto
    'email': 'email',
    ('first_name', 'last_name'): 'nome_usual',
}
```

**IMPORTANTE**: Após alterar, **reinicie o servidor**

### Se Backend não está ativado

Verifique em `settings.py`:
```python
AUTHENTICATION_BACKENDS = [
    "django_suap_auth.backends.SuapAuthBackend",  # ← Deve estar aqui!
    "django.contrib.auth.backends.ModelBackend",
]
```

Se não está, adicione. **Reinicie o servidor**.

## 📍 O Que Procurar nos Logs

```
================================================================================
SUAP CALLBACK - Iniciando fluxo de autenticação
...
1. Validando State (CSRF)
   ✓ State validado com sucesso
2. Trocando código por token de acesso
   ✓ Token obtido com sucesso
3. Buscando informações do usuário no SUAP
   ✓ Informações obtidas com sucesso
   User info keys: ['matricula', 'nome_usual', 'email', ...]    ← PROCURE AQUI
   User info: {'matricula': '12345678', ...}                    ← VEJA AQUI
4. Autenticando usuário no Django
   ✓ Usuário autenticado: 12345678                              ← Se ver ✓ = OK
   ✗ ERRO: authenticate() retornou None                         ← Se ver ✗ = PROBLEMA
5. Redirecionando usuário
   ✓ Redirecionando para: /dashboard/                           ← Fim feliz!
================================================================================
```

## 🚨 Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| State Mismatch | Cookies expirados | Navegador incógnito |
| Failed to exchange code | SECRET expirado | Verifique `.env` |
| Failed to retrieve profile | Scopes insuficientes | SUAP sem acesso |
| authenticate() None | Campo ID não existe | Customize `SUAP_USER_ATTR_MAP` |
| Backend not found | Backend não ativado | Adicione em `AUTHENTICATION_BACKENDS` |

## 📞 Precisa de Ajuda?

1. Compartilhe os **logs completos** do console
2. Diga qual mensagem você vê (erro/sucesso)
3. Procure por "**User info:**" e compartilhe os dados

Vou conseguir ajudar com isso!

## 🎓 Arquivo de Referência Completo

Para entender tudo em detalhes:
- `DIAGNOSTICO_COMPLETO.md` ← Leia isso


