# SUAP OAuth2 Scopes

## Available Scopes

| Scope | Description | Key Attributes |
|-------|-------------|----------------|
| `identificacao` | Basic identification | `matricula`, `nome_usual`, `campus`, `tipo_usuario`, `url_foto_75x100` |
| `email` | Email address | `email` |
| `documentos_pessoais` | Personal documents | `cpf`, `rg` |
| `dados_academicos` | Academic data | `curso`, `situacao`, `periodo_atual` |
| `dados_pessoais` | Personal data | `data_nascimento`, `naturalidade`, `tipo_sanguineo`, `filiacao` |
| `reitoria` | Institution-level data | Institution-specific fields |

## Example SUAP Response

```json
{
  "id": 12345,
  "matricula": "20211234567",
  "nome_usual": "João Silva",
  "cpf": "12345678901",
  "rg": "1234567",
  "filiacao": ["Maria Silva", "José Silva"],
  "data_nascimento": "1995-01-15",
  "naturalidade": "Natal/RN",
  "tipo_sanguineo": "A+",
  "email": "joao.silva@academico.ifrn.edu.br",
  "url_foto_75x100": "https://suap.ifrn.edu.br/media/...",
  "tipo_usuario": "Aluno",
  "campus": "Natal-Central",
  "curso": "Tecnologia em Análise e Desenvolvimento de Sistemas",
  "situacao": "Matriculado"
}
```

## Configuring Scopes

```python
SUAP_AUTH_SCOPES = ["identificacao", "email", "dados_academicos"]
```
