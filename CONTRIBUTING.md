# 🤝 Contributing to Toonkit

¡Gracias por tu interés en contribuir a **toonkit**!

---

## 🚀 Cómo Contribuir

### 1. Setup del Entorno de Desarrollo

```bash
# Fork y clonar
git clone https://github.com/tu-usuario/toonkit.git
cd toonkit

# Instalar con dependencias de desarrollo
pip install -e ".[dev]"

# Verificar instalación
pytest
```

### 2. Crear una Rama

```bash
git checkout -b feature/mi-nueva-feature
# o
git checkout -b fix/mi-bugfix
```

### 3. Hacer Cambios

**Código:**
- Sigue PEP 8 y usa type hints
- Escribe docstrings para funciones públicas
- Mantén funciones pequeñas y cohesivas

**Tests:**
- Añade tests para nueva funcionalidad
- Asegúrate de que todos los tests pasen
- Mantén coverage >90%

```bash
# Ejecutar tests
pytest -v

# Con coverage
pytest --cov=toonkit --cov-report=html
```

### 4. Quality Checks

```bash
# Linting
ruff check toonkit tests

# Formateo
black toonkit tests
isort toonkit tests

# Type checking
mypy toonkit

# O todo de una vez
make quality
```

### 5. Commit y Push

```bash
git add .
git commit -m "feat: agregar funcionalidad X"
git push origin feature/mi-nueva-feature
```

**Formato de commits:**
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `test:` añadir/modificar tests
- `refactor:` refactoring sin cambio de funcionalidad
- `perf:` mejora de performance
- `chore:` mantenimiento (deps, config)

### 6. Abrir Pull Request

1. Ve a GitHub y abre un PR
2. Describe qué cambios hiciste y por qué
3. Referencia issues relacionados
4. Espera review

---

## 📝 Guidelines

### Código

- **Type hints**: Usa tipos en todas las funciones
  ```python
  def encode(data: JsonValue, config: ToonConfig | None = None) -> str:
  ```

- **Docstrings**: Usa formato Google/Numpy
  ```python
  def my_function(arg: str) -> int:
      """
      Short description.
      
      Args:
          arg: Description of argument
          
      Returns:
          Description of return value
          
      Raises:
          ValueError: When X happens
      """
  ```

- **Error handling**: Usa excepciones específicas
  ```python
  if invalid_input:
      raise ToonEncodingError("Descriptive message")
  ```

### Tests

- **Estructura**: Usa classes para agrupar tests relacionados
  ```python
  class TestEncoder:
      def test_simple_case(self) -> None:
          result = encode({"key": "value"})
          assert "key: value" in result
  ```

- **Nombres**: Descriptivos, empezando con `test_`
- **Fixtures**: Usa `conftest.py` para fixtures compartidos
- **Parametrize**: Para múltiples casos similares
  ```python
  @pytest.mark.parametrize("input,expected", [
      (1, "1"),
      (3.14, "3.14"),
      (True, "true"),
  ])
  def test_encode_primitives(input, expected):
      ...
  ```

### Documentación

- README: Actualiza si cambias API pública
- Docstrings: Actualiza si cambias signatures
- CHANGELOG: Añade tu cambio (versión unreleased)

---

## 🐛 Reportar Bugs

**Antes de reportar:**
1. Busca si ya existe el issue
2. Prueba con la última versión
3. Crea un ejemplo mínimo reproducible

**Template:**

```markdown
**Descripción:**
Breve descripción del bug

**Reproducción:**
```python
from toonkit import encode
data = {"problem": "here"}
encode(data)  # Crash!
```

**Expected:** Qué esperabas que pasara
**Actual:** Qué pasó realmente
**Versión:** `toonkit==0.1.0`, Python 3.11
**OS:** Windows/Linux/macOS
```

---

## 💡 Proponer Features

**Template:**

```markdown
**Feature:** Nombre de la feature

**Motivación:** Por qué es útil

**Propuesta:** Cómo funcionaría

**Alternativas:** Otras soluciones consideradas

**Ejemplo de uso:**
```python
from toonkit import nueva_feature
result = nueva_feature(data)
```
```

---

## 🎯 Áreas donde Contribuir

### 🟢 Fácil (Good First Issue)
- Agregar ejemplos de uso
- Mejorar documentación
- Agregar tests para casos edge
- Reportar bugs con reproducción

### 🟡 Intermedio
- Optimizar performance del encoder/decoder
- Agregar soporte para más tokenizadores
- Mejorar mensajes de error
- CLI: nuevos comandos

### 🔴 Avanzado
- Playground web (WASM)
- Schema validation (JSON Schema)
- Plugins para frameworks (LangChain, etc)
- SDKs para otros lenguajes

---

## 📋 Checklist antes de PR

- [ ] Tests pasan (`pytest`)
- [ ] Coverage >90% (`pytest --cov`)
- [ ] Linting OK (`ruff check`)
- [ ] Formateo OK (`black`, `isort`)
- [ ] Type check OK (`mypy`)
- [ ] Docstrings actualizados
- [ ] README actualizado (si aplica)
- [ ] CHANGELOG actualizado

---

## 🏆 Reconocimientos

Todos los contributors serán listados en:
- README (sección Contributors)
- GitHub contributors page
- Release notes

---

## 📞 Preguntas

- **GitHub Discussions**: Para preguntas generales
- **GitHub Issues**: Para bugs/features
- **Email**: info@aedia.com

---

¡Gracias por ayudar a mejorar toonkit! 🎉

