# Fluxo de Autenticação

## Visão Geral

django-suap-auth implementa o fluxo de autorização de código OAuth2.

```mermaid
flowchart TD
    A["🔵 Usuário"] -->|Clica em 'Entrar'| B["GET /auth/suap/login/"]
    B -->|Gera state| C["Armazena state na sessão"]
    C -->|SUAP_AUTH_DIRECT_REDIRECT=True| D["Redireciona para SUAP"]
    C -->|SUAP_AUTH_DIRECT_REDIRECT=False| E["Renderiza página intermediária<br/>login.html"]
    E -->|Usuário clica no botão| D
    D -->|Usuário faz login| F["🔐 SUAP /o/authorize/"]
    F -->|Autoriza acesso| G["Redireciona com code & state"]
    G -->|POST /auth/suap/callback/| H["Valida state<br/>Previne CSRF"]
    H -->|✓ State válido| I["POST /o/token/"]
    H -->|✗ State inválido| J["❌ Erro CSRF<br/>Redireciona para login"]
    I -->|Troca code por token| K["Retorna access_token"]
    K -->|GET /api/rh/eu/| L["🔐 SUAP API"]
    L -->|Retorna dados do usuário| M["{'identificacao': '2080882',<br/>'nome_usual': 'Kelson', ...}"]
    M -->|authenticate()| N["Backend SUAP"]
    N -->|Cria/Atualiza User| O["✅ Usuário autenticado"]
    O -->|login_user()| P["Armazena na sessão"]
    P -->|Redireciona| Q["📍 LOGIN_REDIRECT_URL"]
    Q -->|Ex: /dashboard/| R["✅ Usuário logado<br/>com sucesso"]
    
    style A fill:#e1f5ff
    style F fill:#fff3e0
    style L fill:#fff3e0
    style R fill:#c8e6c9
    style J fill:#ffcdd2
```

## Redirecionamento Direto (Padrão)

Com `SUAP_AUTH_DIRECT_REDIRECT = True` (padrão), o usuário é imediatamente redirecionado para SUAP quando visita `/auth/suap/login/`.

## Página Intermediária

Com `SUAP_AUTH_DIRECT_REDIRECT = False`, a view de login renderiza uma página intermediária (`django_suap_auth/login.html`) onde o usuário deve clicar em um botão para prosseguir para SUAP.

## Proteção CSRF

O parâmetro de estado é gerado usando `secrets.token_urlsafe(32)` e armazenado na sessão. Ele é validado no callback para prevenir ataques CSRF.
