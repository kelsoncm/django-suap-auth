# Attribute Mapping

## Default Mapping

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "email": "email",
    ("first_name", "last_name"): "nome_usual",
}
```

## Custom Mapping

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "email": "email",
    ("first_name", "last_name"): "nome_usual",
    "campus": "campus",  # custom field on your user model
}
```

## Storing Full JSON Response

```python
SUAP_USER_JSON_FIELD = "suap_data"  # JSONField on your user model or profile
```

Or via the attr map:

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "suap_data": "fulljson",  # stores the entire response dict
}
```

## Dotted Key Paths

For nested SUAP response keys:

```python
SUAP_USER_ATTR_MAP = {
    "username": "matricula",
    "data_nascimento": "dados_pessoais.data_nascimento",
}
```

## Name Splitting

When using a tuple key, the SUAP value is split on the first space:

```python
("first_name", "last_name"): "nome_usual"
# "João Silva Santos" → first_name="João", last_name="Silva Santos"
```
