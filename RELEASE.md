# Release management

## Bump version

```bash
bumpver update --minor
```

## Build package

```bash
python -m build
# or
hatch build
```

## Upload to PyPI

```bash
twine check dist/*
# Test
twine upload -r testpypi dist/*
# Production
python -m twine upload dist/*
```
