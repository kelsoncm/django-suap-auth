# Mapeamento de Atributos

O dicionário `USER_ATTR_MAP` define como os campos retornados pelo SUAP são gravados
no model `User` do Django.

## Mapeamento Padrão

```python
SUAP_AUTH = {
    # ...
    'USER_ATTR_MAP': {
        'username': 'identificacao',
        'email': 'email',
        ('first_name', 'last_name'): 'nome_usual',
    },
}
```

## Campo Simples

```python
'USER_ATTR_MAP': {
    'username': 'identificacao',
    'email': 'email',
}
```

## Divisão de Nome em Dois Campos

Quando a chave é uma **tupla**, o valor SUAP é dividido no primeiro espaço:

```python
('first_name', 'last_name'): 'nome_usual'
# "João Silva Santos" → first_name="João", last_name="Silva Santos"
# "João"              → first_name="João", last_name=""
```

## Caminhos de Chave Pontilhados (Aninhados)

Para acessar campos aninhados na resposta JSON do SUAP:

```python
'USER_ATTR_MAP': {
    'username': 'identificacao',
    'data_nascimento': 'dados_pessoais.data_nascimento',
}
```

## Armazenando a Resposta JSON Completa

Use `USER_JSON_FIELD` para gravar o dicionário completo retornado pelo SUAP em um
`JSONField` do seu model:

```python
SUAP_AUTH = {
    # ...
    'USER_JSON_FIELD': 'suap_data',  # JSONField no seu model de usuário
}
```
