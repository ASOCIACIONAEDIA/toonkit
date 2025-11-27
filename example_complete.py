#!/usr/bin/env python3
"""
TOONKIT - Complete Usage Example / Ejemplo Completo de Uso
===========================================================

Este script demuestra todas las características de la librería toonkit.
This script demonstrates all features of the toonkit library.

Casos de Uso / Use Cases:
+ APIs eficientes en tokens (LLMs) / Token-efficient APIs (LLMs)
+ Archivos de configuración / Configuration files
+ Serializacion de datos / Data serialization

IMPORTANTE / IMPORTANT:
Este archivo muestra como TOON reduce dramaticamente el tamaño de contextos
enviados a modelos de IA (GPT, Claude, Gemini, etc), ahorrando dinero real.
This file shows how TOON dramatically reduces the size of contexts sent to
AI models (GPT, Claude, Gemini, etc), saving real money.
"""

import json
from toonkit import encode, decode, encode_streaming, decode_streaming
from toonkit.core.types import ToonConfig, ParserMode


def separator(title_es: str, title_en: str) -> None:
    """Imprime un separador bilingue / Prints bilingual separator"""
    print(f"\n{'='*80}\n  - {title_es}\n  - {title_en}\n{'='*80}\n")


# ============================================================================
# EJEMPLO 1 / EXAMPLE 1: Codificación Básica / Basic Encoding
# ============================================================================

def example_1():
    """Demuestra codificación y decodificación básica"""
    separator(
        "Ejemplo 1: Codificación Básica",
        "Example 1: Basic Encoding"
    )
    
    user = {
        "name": "Alice",
        "age": 28,
        "email": "alice@example.com",
        "active": True,
        "balance": None
    }
    
    print("[DATA] Datos originales / Original data:")
    print(json.dumps(user, indent=2))
    
    # Codificar / Encode
    toon = encode(user)
    print("\n[TOON] Formato TOON:")
    print(toon)
    
    # Decodificar / Decode
    decoded = decode(toon)
    print(f"\n[OK] Coinciden / Match: {user == decoded}")


# ============================================================================
# EJEMPLO 2 / EXAMPLE 2: Arrays y Anidamiento
# ============================================================================

def example_2():
    """Demuestra arrays y estructuras anidadas"""
    separator(
        "Ejemplo 2: Arrays & Estructuras Anidadas",
        "Example 2: Arrays & Nested Structures"
    )
    
    company = {
        "name": "TechCorp",
        "employees": [
            {"id": 1, "name": "Alice", "role": "Engineer"},
            {"id": 2, "name": "Bob", "role": "Manager"}
        ],
        "departments": {
            "eng": {"budget": 500000, "team": 50},
            "sales": {"budget": 300000, "team": 30}
        }
    }
    
    print("[DATA] Estructura anidada / Nested structure:")
    print(json.dumps(company, indent=2))
    
    toon = encode(company)
    print("\n[TOON] Formato TOON:")
    print(toon)
    
    # Comparar tamaños / Compare sizes
    json_size = len(json.dumps(company))
    toon_size = len(toon)
    savings = (1 - toon_size/json_size) * 100
    
    print(f"\n[STATS] Comparacion / Comparison:")
    print(f"  JSON: {json_size} bytes")
    print(f"  TOON: {toon_size} bytes")
    print(f"  Ahorro / Saved: {savings:.1f}%")


# ============================================================================
# EJEMPLO 3 / EXAMPLE 3: Arrays Tabulares (MÁS EFICIENTE)
# ============================================================================

def example_3():
    """Demuestra arrays tabulares - el formato más compacto"""
    separator(
        "Ejemplo 3: Arrays Tabulares (Muy Eficiente)",
        "Example 3: Tabular Arrays (Most Efficient)"
    )
    
    sales = {
        "records": [
            {"id": 1001, "product": "Widget A", "qty": 50, "price": 29.99},
            {"id": 1002, "product": "Widget B", "qty": 75, "price": 19.99},
            {"id": 1003, "product": "Widget C", "qty": 30, "price": 49.99}
        ]
    }
    
    print("[DATA] Datos de ventas / Sales data:")
    print(json.dumps(sales, indent=2))
    
    toon = encode(sales)
    print("\n[TOON] Formato TOON (nota la sintaxis tabular / note tabular syntax):")
    print(toon)
    
    print("\n[INFO] Explicacion / Explanation:")
    print("  records[3]{id,product,qty,price}:")
    print("    [3] = 3 filas / 3 rows")
    print("    {id,product,qty,price} = nombres de columnas / column names")
    print("    Las filas tienen valores separados por comas / Rows have comma-separated values")
    
    # Comparar tamaños / Compare sizes
    json_size = len(json.dumps(sales))
    toon_size = len(toon)
    savings = (1 - toon_size/json_size) * 100
    
    print(f"\n[STATS] Reduccion de tamaño / Size reduction: {savings:.1f}%")
    print(f"  JSON: {json_size} bytes -> TOON: {toon_size} bytes")


# ============================================================================
# EJEMPLO 4 / EXAMPLE 4: Configuración
# ============================================================================

def example_4():
    """Demuestra uso como archivo de configuración"""
    separator(
        "Ejemplo 4: Archivo de Configuración",
        "Example 4: Configuration File"
    )
    
    config_text = """
app: MyApp
version: 1.2.0
debug: false

database:
  host: db.example.com
  port: 5432
  pool_size: 10

api:
  endpoints[2]{url,timeout}:
    https://api.service1.com,30
    https://api.service2.com,60

features:
  - auth
  - analytics
  - notifications
"""
    
    print("[DATA] Archivo de configuracion / Configuration file:")
    print(config_text)
    
    # Decodificar / Decode
    config = decode(config_text)
    print("\n[OK] Configuracion decodificada / Decoded configuration:")
    print(f"  App: {config['app']} v{config['version']}")
    print(f"  Debug: {config['debug']}")
    print(f"  Database: {config['database']['host']}:{config['database']['port']}")
    print(f"  API endpoints: {len(config['api']['endpoints'])}")
    print(f"  Features: {', '.join(config['features'])}")


# ============================================================================
# EJEMPLO 5 / EXAMPLE 5: Caracteres Especiales
# ============================================================================

def example_5():
    """Demuestra manejo de caracteres especiales"""
    separator(
        "Ejemplo 5: Caracteres Especiales",
        "Example 5: Special Characters"
    )
    
    data = {
        "quoted": 'Dijo "Hola" / Said "Hello"',
        "newline": "Linea 1 / Line 1\nLinea 2 / Line 2",
        "colon": "clave: valor / key: value",
        "unicode": "Hola World / Hello World",
        "path": "C:\\Users\\file.txt"
    }
    
    print("[DATA] Datos con caracteres especiales / Data with special characters:")
    print(json.dumps(data, indent=2))
    
    toon = encode(data)
    print("\n[TOON] Formato TOON (con escaping / with escaping):")
    print(toon)
    
    decoded = decode(toon)
    print(f"\n[OK] Caracteres preservados / Characters preserved: {data == decoded}")


# ============================================================================
# EJEMPLO 6 / EXAMPLE 6: Modos de Parser
# ============================================================================

def example_6():
    """Demuestra modos Strict vs Permissive"""
    separator(
        "Ejemplo 6: Modos de Parser",
        "Example 6: Parser Modes"
    )
    
    malformed = """
user:
   name: Alice
       age: 30
"""
    
    print("[DATA] Entrada malformada / Malformed input (over-indented):")
    print(malformed)
    
    # STRICT mode
    print("\n[STRICT] Modo STRICT (fallara / will fail):")
    try:
        strict = ToonConfig(mode=ParserMode.STRICT)
        result = decode(malformed, strict)
    except Exception as e:
        print(f"  [ERR] Error (esperado / expected): Indentacion incorrecta / Incorrect indentation")
    
    # PERMISSIVE mode
    print("\n[PERMISSIVE] Modo PERMISSIVE (intenta parsear / will try to parse):")
    try:
        permissive = ToonConfig(mode=ParserMode.PERMISSIVE)
        result = decode(malformed, permissive)
        print(f"  [OK] Parseado / Parsed: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"  Error: {e}")


# ============================================================================
# EJEMPLO 7 / EXAMPLE 7: Benchmarking
# ============================================================================

def example_7():
    """Compara eficiencia entre JSON y TOON"""
    separator(
        "Ejemplo 7: Benchmarking - JSON vs TOON",
        "Example 7: Benchmarking - JSON vs TOON"
    )
    
    # Generar datos grandes / Generate large dataset
    users = {
        "users": [
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "active": True,
                "role": "admin" if i % 10 == 0 else "user"
            }
            for i in range(100)
        ]
    }
    
    json_str = json.dumps(users)
    toon_str = encode(users)
    
    json_size = len(json_str)
    toon_size = len(toon_str)
    savings = (1 - toon_size/json_size) * 100
    
    print(f"[BENCH] Benchmark con {len(users['users'])} usuarios / users:")
    print(f"  JSON: {json_size:,} bytes")
    print(f"  TOON: {toon_size:,} bytes")
    print(f"  Ahorro / Saved: {savings:.1f}%")
    
    # Estimacion de tokens (1 token aprox 4 bytes)
    json_tokens = json_size / 4
    toon_tokens = toon_size / 4
    tokens_saved = json_tokens - toon_tokens
    
    print(f"\n[TOKENS] Estimacion de tokens / Token estimation (1 token aprox 4 bytes):")
    print(f"  JSON tokens: {json_tokens:.0f}")
    print(f"  TOON tokens: {toon_tokens:.0f}")
    print(f"  Tokens ahorrados / Saved: {tokens_saved:.0f}")
    print(f"\n  Si $0.01 por 1K tokens / If $0.01 per 1K tokens:")
    print(f"  Ahorro por request / Per request: ${tokens_saved/1000*0.01:.4f}")
    print(f"  Ahorro por 1M requests / Per 1M requests: ${tokens_saved/1000*0.01*1_000_000:.2f}")


# ============================================================================
# EJEMPLO 8 / EXAMPLE 8: Streaming
# ============================================================================

def example_8():
    """Demuestra procesamiento en streaming"""
    separator(
        "Ejemplo 8: Procesamiento en Streaming",
        "Example 8: Streaming Processing"
    )
    
    data = {
        "items": [
            {"id": 1, "value": 10, "status": "active"},
            {"id": 2, "value": 20, "status": "inactive"},
            {"id": 3, "value": 30, "status": "active"}
        ]
    }
    
    print("[DATA] Datos originales / Original data:")
    print(json.dumps(data, indent=2))
    
    # Streaming encode
    print("\n[STREAM] Codificacion en streaming (linea por linea / line by line):")
    lines = list(encode_streaming(data))
    for i, line in enumerate(lines, 1):
        print(f"  Linea {i} / Line {i}: {line}")
    
    # Streaming decode
    print("\n[STREAM] Decodificacion en streaming...")
    decoded = decode_streaming(iter(lines))
    print(f"  [OK] Decodificado correctamente / Decoded correctly: {data == decoded}")


# ============================================================================
# EJEMPLO 9 / EXAMPLE 9: Caso Real
# ============================================================================

def example_9():
    """Demuestra un caso de uso real"""
    separator(
        "Ejemplo 9: Caso de Uso Real - Pipeline de Datos",
        "Example 9: Real-World Use Case - Data Pipeline"
    )
    
    print("[SCENARIO] Escenario / Scenario:")
    print("  Procesar analytics de usuarios eficientemente")
    print("  Processing user analytics data efficiently\n")
    
    analytics = {
        "period": "2024-01",
        "summary": {
            "total_users": 15000,
            "new_users": 2345,
            "sessions": 8934
        },
        "events": [
            {"timestamp": "2024-01-01T10:00:00", "event": "login", "count": 1234},
            {"timestamp": "2024-01-01T10:05:00", "event": "page_view", "count": 5678},
            {"timestamp": "2024-01-01T10:10:00", "event": "purchase", "count": 234}
        ]
    }
    
    print("[DATA] Datos de analytics / Analytics data:")
    print(json.dumps(analytics, indent=2))
    
    # Serializar / Serialize
    serialized = encode(analytics)
    print("\n[ENCODED] Serializado / Serialized:")
    print(serialized)
    
    # Calcular ahorros / Calculate savings
    json_size = len(json.dumps(analytics))
    toon_size = len(serialized)
    
    print(f"\n[REPORT] Reporte de Eficiencia / Efficiency Report:")
    print(f"  JSON: {json_size} bytes")
    print(f"  TOON: {toon_size} bytes")
    print(f"  Ahorro / Saved: {(1-toon_size/json_size)*100:.1f}%")
    
    requests_per_month = 1_000_000
    bytes_saved = (json_size - toon_size) * requests_per_month
    print(f"\n  Con {requests_per_month:,} requests/mes:")
    print(f"  Bytes ahorrados / Bytes saved: {bytes_saved/1024/1024:.2f} MB")


# ============================================================================
# EJEMPLO 10 / EXAMPLE 10: Configuración Personalizada
# ============================================================================

def example_10():
    """Demuestra opciones de configuración"""
    separator(
        "Ejemplo 10: Configuración Personalizada",
        "Example 10: Custom Configuration"
    )
    
    data = {
        "user": "alice",
        "settings": {
            "theme": "dark",
            "notifications": True
        }
    }
    
    print("[DATA] Datos originales / Original data:")
    print(json.dumps(data, indent=2))
    
    # Por defecto / Default
    print("\n[CONFIG] Codificacion por defecto / Default:")
    default = encode(data)
    print(default)
    
    # Sin ordenar keys / Unsorted keys
    print("\n[CONFIG] Sin ordenar keys / Unsorted keys:")
    unsorted = encode(data, ToonConfig(sort_keys=False))
    print(unsorted)
    
    # Indentacion custom / Custom indent - nota: debe usarse el mismo indent para decodificar
    print("\n[CONFIG] Indentacion custom (4 espacios / 4 spaces):")
    custom = encode(data, ToonConfig(indent_size=4))
    print(custom)
    custom_config = ToonConfig(indent_size=4)
    
    print("\n[OK] Todas decodifican correctamente / All decode correctly:")
    print(f"  Default: {decode(default) == data}")
    print(f"  Unsorted: {decode(unsorted) == data}")
    print(f"  Custom: {decode(custom, custom_config) == data}")


# ============================================================================
# EJEMPLO 11 / EXAMPLE 11: OpenAI GPT-4 con contexto en TOON
# ============================================================================

def example_11():
    """
    Demuestra como reducir drasticamente el costo de llamadas a GPT-4
    Demonstrates how to drastically reduce GPT-4 API call costs
    """
    separator(
        "Ejemplo 11: OpenAI GPT-4 - Contexto Eficiente en Tokens",
        "Example 11: OpenAI GPT-4 - Token-Efficient Context"
    )
    
    # Contexto largo / Long context
    conversation_data = {
        "user_profile": {
            "id": 12345,
            "name": "Carlos Perez",
            "email": "carlos@example.com",
            "tier": "premium",
            "created": "2023-01-15",
            "preferences": {
                "language": "es",
                "notifications": True,
                "theme": "dark"
            }
        },
        "conversation_history": [
            {"role": "user", "content": "Hola, necesito ayuda con mi cuenta"},
            {"role": "assistant", "content": "Claro, estoy aqui para ayudarte"},
            {"role": "user", "content": "Quiero cambiar mi contraseña"},
            {"role": "assistant", "content": "Por supuesto, te guiare en el proceso"}
        ],
        "support_tickets": [
            {"id": 101, "date": "2024-01", "issue": "billing", "resolved": True},
            {"id": 102, "date": "2024-02", "issue": "feature_request", "resolved": False},
            {"id": 103, "date": "2024-03", "issue": "bug_report", "resolved": True}
        ],
        "transactions": [
            {"date": "2024-01-15", "type": "subscription", "amount": 99.99, "status": "paid"},
            {"date": "2024-02-15", "type": "subscription", "amount": 99.99, "status": "paid"},
            {"date": "2024-03-15", "type": "subscription", "amount": 99.99, "status": "paid"}
        ]
    }
    
    # Sistema de prompts / System prompts
    system_instruction = """You are a premium customer support AI for a SaaS platform.
Use the provided context to personalize responses and solve customer issues efficiently.
Always maintain a professional yet friendly tone in Spanish when the user is Spanish-speaking.
Consider the user's tier, history, and previous interactions when crafting responses."""
    
    # Crear mensaje para OpenAI / Create OpenAI message
    json_version = json.dumps(conversation_data)
    toon_version = encode(conversation_data)
    
    # Calcular ahorros / Calculate savings
    json_size = len(json_version)
    toon_size = len(toon_version)
    reduction = (1 - toon_size/json_size) * 100
    
    print("[CONTEXT] JSON vs TOON para enviar a OpenAI:")
    print(f"\nJSON (original): {json_size} bytes")
    print("---")
    print(json_version[:200] + "...")
    
    print(f"\nTOON (comprimido): {toon_size} bytes")
    print("---")
    print(toon_version[:200] + "...")
    
    # Estimacion de costos / Cost estimation
    json_tokens = json_size / 4
    toon_tokens = toon_size / 4
    tokens_saved = json_tokens - toon_tokens
    
    print(f"\n[COST] Estimacion de costos / Cost estimation:")
    print(f"  Contexto JSON / JSON context: {json_tokens:.0f} tokens")
    print(f"  Contexto TOON / TOON context: {toon_tokens:.0f} tokens")
    print(f"  Tokens ahorrados / Saved: {tokens_saved:.0f}")
    
    print(f"\n  Tarifa OpenAI GPT-4 Turbo: $0.01 por 1K input tokens")
    print(f"  OpenAI GPT-4 Turbo rate: $0.01 per 1K input tokens")
    
    cost_json = json_tokens / 1000 * 0.01
    cost_toon = toon_tokens / 1000 * 0.01
    cost_saved = cost_json - cost_toon
    
    print(f"\n  Costo por llamada JSON / Cost per JSON call: ${cost_json:.4f}")
    print(f"  Costo por llamada TOON / Cost per TOON call: ${cost_toon:.4f}")
    print(f"  Ahorro por llamada / Saved per call: ${cost_saved:.4f}")
    print(f"  Ahorro por 1M llamadas / Saved per 1M calls: ${cost_saved * 1_000_000:.2f}")
    
    print(f"\n[EJEMPLO] Mensaje para enviar a OpenAI / Message to send to OpenAI:")
    print("---")
    print(f"""messages = [
    {{"role": "system", "content": "{system_instruction[:60]}..."}},
    {{"role": "user", "content": "Hola, necesito cambiar mi contraseña"}},
    {{"role": "user", "content": "context_json: " + toon_compressed_data}}
]
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=messages
)""")


# ============================================================================
# EJEMPLO 12 / EXAMPLE 12: Claude (Anthropic) con Archivos Adjuntos
# ============================================================================

def example_12():
    """
    Demuestra como usar TOON con Claude API y archivos adjuntos
    Shows how to use TOON with Claude API and file attachments
    """
    separator(
        "Ejemplo 12: Claude API - Archivos Estructurados Eficientes",
        "Example 12: Claude API - Efficient Structured Files"
    )
    
    # Dataset grande / Large dataset
    user_analytics = {
        "report_date": "2024-03-27",
        "summary": {
            "total_users": 50000,
            "active_users": 35000,
            "new_users": 5000,
            "churn_rate": 0.02
        },
        "daily_metrics": [
            {"date": "2024-03-21", "active": 34500, "new": 450, "revenue": 12500},
            {"date": "2024-03-22", "active": 34800, "new": 480, "revenue": 13200},
            {"date": "2024-03-23", "active": 35100, "new": 520, "revenue": 14100},
            {"date": "2024-03-24", "active": 35200, "new": 510, "revenue": 13800},
            {"date": "2024-03-25", "active": 35300, "new": 530, "revenue": 14500},
            {"date": "2024-03-26", "active": 35400, "new": 550, "revenue": 15000},
            {"date": "2024-03-27", "active": 35000, "new": 200, "revenue": 8500}
        ],
        "cohorts": {
            "2024-01": {"retention": [100, 85, 72, 65], "ltv": 450},
            "2024-02": {"retention": [100, 87, 75, 68], "ltv": 500},
            "2024-03": {"retention": [100, 89, 78], "ltv": 520}
        }
    }
    
    # Crear versiones / Create versions
    json_file = json.dumps(user_analytics, indent=2)
    toon_file = encode(user_analytics)
    
    json_size = len(json_file)
    toon_size = len(toon_file)
    reduction = (1 - toon_size/json_size) * 100
    
    print("[FILE] Archivo de datos para Claude / Data file for Claude:")
    print(f"\nJSON: {json_size} bytes")
    print(json_file[:250] + "...")
    
    print(f"\nTOON: {toon_size} bytes (ahorro / saved: {reduction:.1f}%)")
    print(toon_file[:250] + "...")
    
    # Calcular ahorro en contexto / Calculate context savings
    json_tokens = json_size / 4
    toon_tokens = toon_size / 4
    tokens_saved = json_tokens - toon_tokens
    
    print(f"\n[CLAUDE_API] Tarifa de Claude 3 Opus:")
    print(f"  Input: $0.015 per 1K tokens")
    print(f"  Output: $0.075 per 1K tokens")
    
    input_cost_json = json_tokens / 1000 * 0.015
    input_cost_toon = toon_tokens / 1000 * 0.015
    input_saved = input_cost_json - input_cost_toon
    
    print(f"\n  Costo input JSON / JSON input cost: ${input_cost_json:.4f}")
    print(f"  Costo input TOON / TOON input cost: ${input_cost_toon:.4f}")
    print(f"  Ahorro / Saved: ${input_saved:.4f} por request")
    print(f"  Ahorro anual / Annual savings (10M requests): ${input_saved * 10_000_000:.2f}")
    
    print(f"\n[USAGE] Como usar en Claude / How to use in Claude:")
    print("---")
    print(f"""# Opcion 1: Enviar TOON directamente / Direct TOON
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {{
            "role": "user",
            "content": "Analiza estos datos (formato TOON comprimido):\\n{toon_file[:100]}..."
        }}
    ]
)

# Opcion 2: Con FILES API / With FILES API
response = client.beta.files.upload(
    file=("analytics.toon", toon_file),
)
message = client.beta.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{{"role": "user", "content": "Analiza el archivo adjunto"}}],
    files=[response.id]
)""")


# ============================================================================
# EJEMPLO 13 / EXAMPLE 13: Comparacion de LLMs - Ahorro Total
# ============================================================================

def example_13():
    """
    Comparacion de ahorros en diferentes modelos de IA
    Comparison of savings across different AI models
    """
    separator(
        "Ejemplo 13: Comparacion de Ahorros en Diferentes LLMs",
        "Example 13: Savings Comparison Across Different LLMs"
    )
    
    # Dataset mediano / Medium dataset
    large_context = {
        "query": "Analiza el comportamiento de usuarios en la plataforma",
        "user_segments": [
            {"id": i, "age": 25+i*2, "country": "ES", "ltv": 500+i*50, "churn_risk": i%3==0}
            for i in range(100)
        ],
        "metrics": {
            "dau": 50000, "mau": 200000, "retention_d1": 0.65, "retention_d7": 0.35,
            "arpu": 15.50, "arppu": 45.00, "conversion": 0.025
        }
    }
    
    json_str = json.dumps(large_context)
    toon_str = encode(large_context)
    
    json_tokens = len(json_str) / 4
    toon_tokens = len(toon_str) / 4
    tokens_saved = json_tokens - toon_tokens
    reduction_pct = (1 - len(toon_str)/len(json_str)) * 100
    
    print("[DATASET] Contexto para analisis:")
    print(f"  Tamaño original / Original size: {len(json_str)} bytes ({json_tokens:.0f} tokens)")
    print(f"  Tamaño TOON / TOON size: {len(toon_str)} bytes ({toon_tokens:.0f} tokens)")
    print(f"  Reduccion / Reduction: {reduction_pct:.1f}%\n")
    
    # Comparar modelos / Compare models
    models = [
        {"name": "GPT-4 Turbo", "input": 0.01, "output": 0.03, "calls": 1_000_000},
        {"name": "GPT-3.5 Turbo", "input": 0.0005, "output": 0.0015, "calls": 5_000_000},
        {"name": "Claude 3 Opus", "input": 0.015, "output": 0.075, "calls": 1_000_000},
        {"name": "Claude 3 Sonnet", "input": 0.003, "output": 0.015, "calls": 2_000_000},
        {"name": "Gemini Pro", "input": 0.00025, "output": 0.0005, "calls": 10_000_000},
    ]
    
    print("[COMPARISON] Ahorro anual por modelo / Annual savings by model:")
    print("-" * 90)
    print(f"{'Modelo':<20} {'Input Cost':<15} {'Annual Calls':<15} {'Ahorro TOON':<15}")
    print("-" * 90)
    
    total_savings = 0
    for model in models:
        input_cost_json = json_tokens / 1000 * model["input"] * model["calls"]
        input_cost_toon = toon_tokens / 1000 * model["input"] * model["calls"]
        annual_savings = input_cost_json - input_cost_toon
        total_savings += annual_savings
        
        print(f"{model['name']:<20} ${model['input']*1000:>6.4f}/1k  {model['calls']:>12,} calls  ${annual_savings:>12,.2f}")
    
    print("-" * 90)
    print(f"{'TOTAL ANNUAL SAVINGS':<20} {'':15} {'':15} ${total_savings:>12,.2f}")
    print("-" * 90)
    
    print(f"\n[NOTA] Con TOON en un sistema multi-LLM:")
    print(f"  Ahorros anuales / Annual savings: ${total_savings:,.2f}")
    print(f"  Reduccion de latencia / Latency reduction: ~{reduction_pct:.0f}%")
    print(f"  Mejor escalabilidad / Better scalability")
    print(f"  Menor uso de ancho de banda / Lower bandwidth usage")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecutar todos los ejemplos / Run all examples"""
    
    print("\n" + "="*80)
    print("  TOONKIT - Guia Completa de Uso")
    print("  TOONKIT - Complete Usage Guide")
    print("  Serializacion eficiente para APIs y LLMs")
    print("  Efficient serialization for APIs and LLMs")
    print("="*80)
    
    examples = [
        example_1,
        example_2,
        example_3,
        example_4,
        example_5,
        example_6,
        example_7,
        example_8,
        example_9,
        example_10,
        example_11,
        example_12,
        example_13,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n[ERR] Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("  OK Todos los ejemplos completados")
    print("  OK All examples completed!")
    print("  Documentacion / Documentation: https://github.com/ASOCIACIONAEDIA/toonkit")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
