# Política de Segurança

## Versões Suportadas

| Versão | Suportada          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Relatando uma Vulnerabilidade

Se você descobrir uma vulnerabilidade de segurança no django-suap-auth, por favor relate-a abrindo um [Aviso de Segurança do GitHub](https://github.com/kelsoncm/django-suap-auth/security/advisories/new).

**Por favor, não relate vulnerabilidades de segurança através de issues públicas do GitHub.**

Reconheceremos seu relatório dentro de 48 horas e forneceremos uma resposta mais detalhada dentro de 7 dias. Se o problema for confirmado, lançaremos um patch o mais rápido possível.

## Considerações de Segurança

- O parâmetro de estado OAuth2 é validado em cada callback para prevenir ataques CSRF.
- Tokens de acesso nunca são armazenados; eles são trocados imediatamente por informações do usuário.
- Segredos do cliente devem ser mantidos fora do controle de versão.
- Sempre use HTTPS em produção (`SUAP_REDIRECT_URI` deve usar HTTPS em produção).
