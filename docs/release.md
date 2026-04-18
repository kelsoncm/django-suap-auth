# Release Process

## Versioning

This project follows [Semantic Versioning](https://semver.org/).

## Steps

1. Update `version` in `pyproject.toml`
2. Update the changelog
3. Create a git tag: `git tag v0.1.0`
4. Push the tag: `git push origin v0.1.0`
5. The `publish.yml` GitHub Actions workflow will automatically publish to PyPI via Trusted Publisher

## Trusted Publisher

PyPI publication uses GitHub Actions [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) — no secrets needed.
