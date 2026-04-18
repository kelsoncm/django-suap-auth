# Mapeamento de Atributos

## Mapeamento Padrão

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "email": "email",
    ("first_name", "last_name"): "nome_usual",
}
```

## Mapeamento Personalizado

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "email": "email",
    ("first_name", "last_name"): "nome_usual",
    "campus": "campus",  # campo personalizado no seu modelo de usuário
}
```

## Armazenando a Resposta JSON Completa

```python
SUAP_USER_JSON_FIELD = "suap_data"  # JSONField no seu modelo de usuário ou perfil
```

Ou via o mapa de atributos:

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "suap_data": "fulljson",  # armazena o dicionário de resposta completo
}
```

## Caminhos de Chave Pontilhados

Para chaves de resposta SUAP aninhadas:

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "data_nascimento": "dados_pessoais.data_nascimento",
}
```

## Divisão de Nome

Quando usar uma chave tupla, o valor SUAP é dividido no primeiro espaço:

```python
("first_name", "last_name"): "nome_usual"
# "João Silva Santos" → first_name="João", last_name="Silva Santos"
```
