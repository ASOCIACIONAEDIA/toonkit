# 🚀 Quickstart - Toonkit

Guía rápida de 5 minutos para empezar con **toonkit**.

---

## Instalación

```bash
pip install toonkit
```

---

## 1. Conversión Básica

```python
from toonkit import encode, decode

# Tu data JSON
data = {
    "users": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"}
    ]
}

# JSON → TOON (ahorra tokens)
toon = encode(data)
print(toon)
# Output:
# users[2]{id,name,role}:
#   1,Alice,admin
#   2,Bob,user

# TOON → JSON (recupera los datos)
original = decode(toon)
assert original == data  # ✅ Idéntico
```

---

## 2. CLI Rápida

```bash
# Convertir archivo
toonkit convert data.json -o data.toon

# Benchmark (ver ahorro de tokens)
toonkit benchmark data.json -m gpt-4

# Validar round-trip
toonkit validate data.json
```

---

## 3. Benchmark en Código

```python
from toonkit.benchmark import TokenBenchmark

benchmark = TokenBenchmark()
result = benchmark.compare(data, model="gpt-4")

print(f"Tokens ahorrados: {result.token_reduction_pct:.1f}%")
# Output: Tokens ahorrados: 42.0% 🚀
```

---

## 4. Caso de Uso Real: LLM Prompt

```python
from toonkit import encode
import openai

# Data grande de una API
api_data = fetch_products_from_db()  # 100 productos

# Convertir a TOON antes de enviar al LLM
toon_prompt = encode(api_data)

# Enviar a OpenAI (ahorra 40% de tokens = 40% menos costo)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Analiza estos productos:"},
        {"role": "user", "content": toon_prompt}
    ]
)

# El modelo entiende TOON perfectamente y responde
print(response.choices[0].message.content)
```

**Ahorro típico**: 
- 1,000 tokens → 600 tokens
- $0.03 → $0.018 por request
- $30,000 → $18,000 por millón de requests

---

## 5. Configuración Avanzada

```python
from toonkit import ToonConfig, ParserMode

config = ToonConfig(
    sort_keys=True,           # Orden canónico (para caching)
    mode=ParserMode.STRICT,   # Validación estricta
    max_depth=10,             # Límite de anidamiento
    max_size_mb=50,           # Límite de tamaño
)

toon = encode(data, config)
```

---

## 6. Streaming para Datasets Grandes

```python
from toonkit import encode_streaming

# Encode línea por línea (ideal para >100MB)
for line in encode_streaming(massive_dataset):
    socket.send(line)  # Envía progresivamente
```

---

## Próximos Pasos

- 📖 Lee el [README completo](README.md)
- 🧪 Ejecuta los [ejemplos](examples/)
- 🧪 Prueba tus propios datos
- 📊 Mide el ahorro con `toonkit benchmark`

---

**¿Preguntas?** Abre un issue en GitHub o lee la [documentación completa](README.md).

🎉 **¡Empieza a ahorrar tokens hoy!**

