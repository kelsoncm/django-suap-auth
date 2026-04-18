# Processo de Lançamento

## Versionamento

Este projeto segue [Versionamento Semântico](https://semver.org/).

## Etapas

1. Atualizar `version` em `pyproject.toml`
2. Atualizar o changelog
3. Criar uma tag git: `git tag v0.1.0`
4. Enviar a tag: `git push origin v0.1.0`
5. O workflow `publish.yml` do GitHub Actions publicará automaticamente no PyPI via Trusted Publisher

## Trusted Publisher

A publicação no PyPI usa [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) do GitHub Actions — nenhum segredo necessário.
