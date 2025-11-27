# 📦 Guía de Publicación en PyPI

Instrucciones paso a paso para publicar **toonkit** en PyPI.

---

## ✅ Status Actual (v0.1.0)

✅ **TOONKIT ya está publicado en PyPI!**

- 📦 PyPI: https://pypi.org/project/toonkit/
- 📥 Instalar: `pip install toonkit`
- 📊 Tests: 62 tests passing, 68% coverage
- 🚀 Versión: 0.1.0 (Beta)

---

## 🔧 Setup Local

### 1. Instalar Herramientas

```bash
pip install --upgrade pip
pip install build twine
```

### 2. Configurar Credenciales

Crea o edita `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEI...  # Tu token de PyPI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...  # Tu token de TestPyPI
```

**Permisos:**

```bash
chmod 600 ~/.pypirc
```

---

## 🧪 Pre-publicación: Tests y Quality

### 1. Verificar que Todo Funciona

```bash
# Tests
make test-cov

# Quality checks
make quality

# Build local
make build
```

Asegúrate de que:
- ✅ Todos los tests pasan
- ✅ Coverage >90%
- ✅ Sin errores de linting
- ✅ Sin errores de mypy

### 2. Actualizar Versión

En `pyproject.toml`:

```toml
[project]
version = "0.1.0"  # Actualizar según Semantic Versioning
```

### 3. Actualizar CHANGELOG

En `CHANGELOG.md`:

```markdown
## [0.1.0] - 2024-01-20

### Added
- Initial release
- Core features...
```

### 4. Commit de Release

```bash
git add .
git commit -m "chore: release v0.1.0"
git tag v0.1.0
git push origin main --tags
```

---

## 🧪 Publicar en TestPyPI (Recomendado Primero)

### 1. Build

```bash
# Limpiar builds anteriores
make clean

# Build nuevo
python -m build
```

Esto crea:
- `dist/toonkit-0.1.0-py3-none-any.whl`
- `dist/toonkit-0.1.0.tar.gz`

### 2. Verificar Distribución

```bash
twine check dist/*
```

Output esperado:
```
Checking dist/toonkit-0.1.0-py3-none-any.whl: PASSED
Checking dist/toonkit-0.1.0.tar.gz: PASSED
```

### 3. Upload a TestPyPI

```bash
twine upload --repository testpypi dist/*
```

O con el Makefile:

```bash
make publish-test
```

### 4. Probar Instalación desde TestPyPI

```bash
# En un nuevo virtualenv
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Instalar desde TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple toonkit

# Probar
python -c "from toonkit import encode; print(encode({'test': 42}))"

# Output esperado:
# test: 42
```

Si todo funciona, ¡listo para producción! 🎉

---

## 🚀 Publicar en PyPI (Producción)

### 1. Build Final

```bash
make clean
python -m build
twine check dist/*
```

### 2. Upload a PyPI

```bash
twine upload dist/*
```

O con el Makefile:

```bash
make publish
```

### 3. Verificar en PyPI

1. Ve a https://pypi.org/project/toonkit/
2. Verifica que la página se vea bien
3. Revisa metadata, README, etc.

### 4. Instalar desde PyPI

```bash
# En un nuevo virtualenv
pip install toonkit

# Probar
python -c "from toonkit import encode, decode; print('✅ Funciona!')"
```

### 5. Probar CLI

```bash
toonkit --version
# Output: toonkit, version 0.1.0

toonkit --help
```

---

## 📢 Post-publicación

### 1. Anuncio

- GitHub Release: https://github.com/aedia/toonkit/releases
  - Tag: `v0.1.0`
  - Title: `toonkit v0.1.0 - Initial Release`
  - Description: Copiar de CHANGELOG.md

### 2. Actualizar README

Agregar badge de PyPI:

```markdown
[![PyPI version](https://badge.fury.io/py/toonkit.svg)](https://pypi.org/project/toonkit/)
```

### 3. Redes Sociales (opcional)

- Twitter/X: "🚀 Just published toonkit - reduce LLM tokens by 30-60%!"
- LinkedIn, Reddit (r/python, r/MachineLearning)
- Hacker News

---

## 🔄 Actualizaciones Futuras

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (0.1.0 → 0.2.0): New features, backwards compatible
- **PATCH** (0.1.0 → 0.1.1): Bug fixes

### Workflow de Release

1. Crear rama `release/v0.2.0`
2. Actualizar versión en `pyproject.toml`
3. Actualizar `CHANGELOG.md`
4. PR → main
5. Merge
6. Tag: `git tag v0.2.0`
7. Build y publish
8. GitHub Release

---

## 🐛 Troubleshooting

### Error: "File already exists"

PyPI no permite re-subir la misma versión. Solución:

```bash
# Incrementar versión en pyproject.toml
version = "0.1.1"

# Rebuild y re-upload
make clean build
make publish
```

### Error: "Invalid username or password"

Verifica:
- Token API correcto en `~/.pypirc`
- Username es `__token__` (con doble guion bajo)
- Token empieza con `pypi-`

### Error: "Package metadata is invalid"

```bash
# Verificar con twine
twine check dist/*

# Revisar pyproject.toml
# - README.md existe
# - Campos required completos
# - Versión válida
```

---

## 📋 Checklist de Publicación

Pre-publicación:
- [ ] Tests pasan (100%)
- [ ] Coverage >90%
- [ ] Linting OK
- [ ] Versión actualizada
- [ ] CHANGELOG actualizado
- [ ] README revisado
- [ ] Git tag creado

Publicación:
- [ ] Build OK
- [ ] `twine check` OK
- [ ] TestPyPI OK (opcional)
- [ ] PyPI publicado
- [ ] Instalación verificada
- [ ] CLI funciona

Post-publicación:
- [ ] GitHub Release
- [ ] Badge actualizado
- [ ] Anuncio (si aplica)

---

## 📞 Soporte

Si tienes problemas:

1. Lee la [documentación oficial de PyPI](https://packaging.python.org/tutorials/packaging-projects/)
2. Abre un issue en GitHub
3. Email: info@aedia.com

---

**¡Feliz publicación!** 🎉

