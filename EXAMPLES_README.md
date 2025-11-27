# TOONKIT - Ejemplos de Uso / Usage Examples

Este directorio contiene ejemplos completos de como usar TOONKIT en sistemas reales que integran APIs de IA.

## 📁 Archivos

### 1. `example_complete.py` - Guía Completa Interactiva
**13 ejemplos detallados mostrando todas las características**

```bash
python example_complete.py
```

Incluye:
- Ejemplos 1-10: Características básicas de TOONKIT
- Ejemplo 11: Integración con OpenAI GPT-4 (ahorros reales de costos)
- Ejemplo 12: Integración con Claude API (Anthropic)
- Ejemplo 13: Comparativa de ahorros entre múltiples LLMs

**Output esperado:**
- Demostraciones bilingual (Español/Inglés)
- Cálculos de reducción de tamaño
- Estimaciones de ahorros de costos
- Código de integración listo para usar

---

### 2. `demo_llm_savings.py` - Calculadora de Ahorros
**Calcula ahorros reales en 3 casos de uso diferentes**

```bash
python demo_llm_savings.py
```

Casos analizados:
1. **Sistema de Soporte al Cliente**
   - Contexto: perfiles, historial de conversación, tickets
   - Reducción: ~52%
   - Ahorro anual: $14,227 (con GPT-4 + Claude)
   - ROI: 285% en 4.2 meses

2. **Analytics Pipeline**
   - Contexto: reportes diarios, métricas, eventos
   - Reducción: ~32%
   - Ahorro anual: $2,607
   - ROI: 52% en 23 meses

3. **Document Processing**
   - Contexto: documentos legales con anotaciones
   - Reducción: ~2-3%
   - Ahorro anual: $352

---

### 3. `integration_examples.py` - Ejemplos de Integración Real
**Código listo para copiar/pegar en tus proyectos**

```bash
python integration_examples.py
```

Incluye código para:

#### OpenAI GPT-4
```python
from toonkit import encode

# Antes (caro):
message = {"role": "user", "content": json.dumps(context)}

# Después (barato):
message = {"role": "user", "content": encode(context)}
```

#### Anthropic Claude
```python
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[{
        "role": "user",
        "content": encode(analytics_data)
    }]
)
```

#### Google Gemini
```python
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content(encode(conversation_data))
```

#### Ejemplo Completo con Proyecciones
Simula un CRM enviando contexto de cliente a Claude 10,000 veces/día:
- JSON: $1,098.19/día
- TOON: $808.01/día
- **Ahorro: $290.18/día = $106K/año**

---

## 🚀 Quick Start

```python
from toonkit import encode, decode
import json

# Tu contexto (puede ser muy grande)
context = {
    "user": {...},
    "history": [...],
    "analytics": {...}
}

# Convertir a TOON (más compacto)
compressed = encode(context)

# Enviar a LLM
response = client.messages.create(
    model="gpt-4",
    messages=[{"role": "user", "content": compressed}]
)

# Recuperar datos originales (si es necesario)
original = decode(compressed)
```

---

## 📊 Resultados Típicos

| Caso de Uso | Reducción | Ahorro/Mes | ROI |
|---|---|---|---|
| Customer Support | 51.9% | $1,185 | 285% (4.2 meses) |
| Analytics | 32.4% | $217 | 52% (23 meses) |
| Document Processing | 2.4% | $29 | 7% (170 meses) |
| **CRM a escala** | **26.4%** | **$8,743** | ****475% (7 días)**\*\* |

*\*CRM con 10K llamadas/día a Claude*

---

## 🎯 Cuándo Usar TOONKIT

### ✅ Perfecto para:
- APIs de LLM con contextos largos (OpenAI, Claude, Gemini)
- Sistemas de soporte con historial conversacional
- Pipelines de análisis de datos
- Archivos de configuración comprimidos
- Cualquier contexto enviado a modelos de IA múltiples veces

### ❌ No es ideal para:
- Datos sin estructura
- Objetos muy pequeños (< 100 bytes)
- Cuando la legibilidad humana es crítica

---

## 💾 Instalación

```bash
pip install toonkit
```

---

## 🔗 Referencias

- **GitHub:** https://github.com/cafep/toonkit
- **Documentación:** [Ver PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)
- **Changelog:** [Ver CHANGELOG.md](../CHANGELOG.md)

---

## ❓ FAQ

**P: ¿Qué es TOONKIT?**
R: Es un formato de serialización optimizado para LLMs que reduce tokens en 30-70%.

**P: ¿Es compatible con JSON?**
R: No es JSON, pero es reversible. `encode(data)` → comprimido → `decode()` → datos originales.

**P: ¿Qué LLMs soporta?**
R: Todos - OpenAI, Claude, Gemini, Llama, etc. Solo necesita que acepte texto.

**P: ¿Hay pérdida de datos?**
R: No. TOONKIT es 100% reversible. El round-trip es perfecto.

**P: ¿Cuánto se ahorra?**
R: 30-70% típicamente. Depende de la estructura de datos. Ver ejemplos arriba.

---

Creado con ❤️ para desarrolladores que quieren ahorrar dinero en APIs de IA.
