#!/usr/bin/env python3
"""
TOONKIT - Real Integration Examples / Ejemplos de Integracion Real
==================================================================

Este archivo muestra como integrar TOONKIT en sistemas reales
que usan OpenAI, Claude, Gemini, etc.

Se muestran 3 ejemplos practicos:
1. OpenAI GPT-4 con contexto largo
2. Anthropic Claude con archivos
3. Google Gemini con multi-turn conversations
"""

import json
from toonkit import encode, decode

# ============================================================================
# EJEMPLO 1: OpenAI GPT-4 Integration
# ============================================================================

def example_openai_integration():
    """
    Como usar TOONKIT con OpenAI para ahorrar costos
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: OpenAI GPT-4 Integration")
    print("="*80)
    
    # ANTES: Usando JSON (caro)
    customer_context = {
        "customer_id": "cust_12345",
        "name": "Carlos Perez",
        "email": "carlos@example.com",
        "purchase_history": [
            {"date": "2024-01-15", "product": "Plan Pro", "amount": 99.99},
            {"date": "2024-02-15", "product": "Plan Pro", "amount": 99.99},
            {"date": "2024-03-15", "product": "Plan Pro", "amount": 99.99}
        ],
        "support_tickets": [
            {"id": 1001, "date": "2024-02-01", "topic": "Billing", "status": "resolved"},
            {"id": 1002, "date": "2024-03-10", "topic": "Technical", "status": "open"}
        ]
    }
    
    # Version JSON (ANTES - cara)
    json_context = json.dumps(customer_context)
    json_size = len(json_context)
    json_tokens = json_size / 4
    
    # Version TOON (DESPUES - barata)
    toon_context = encode(customer_context)
    toon_size = len(toon_context)
    toon_tokens = toon_size / 4
    
    print(f"\n[ANTES] JSON: {json_size} bytes = {json_tokens:.0f} tokens")
    print(f"[DESPUES] TOON: {toon_size} bytes = {toon_tokens:.0f} tokens")
    print(f"[AHORRO] {(1-toon_size/json_size)*100:.1f}% reduccion de tokens")
    
    # Mostrar integracion con OpenAI
    print(f"\n[CODIGO] Como integrar con OpenAI:")
    print("""
# Opcion 1: Basico - reemplazar json.dumps() con encode()
import openai
from toonkit import encode

context = {...}  # Tu contexto

# ANTES (caro):
# response = openai.ChatCompletion.create(
#     model="gpt-4-turbo",
#     messages=[{
#         "role": "user",
#         "content": "User: " + json.dumps(context)
#     }]
# )

# DESPUES (barato con TOON):
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "user",
        "content": "Contexto (formato TOON):\\n" + encode(context)
    }]
)

print(response.choices[0].message.content)
""")
    
    savings_per_call = (json_tokens - toon_tokens) / 1000 * 0.01
    print(f"\n[AHORRO] Costo: ${savings_per_call:.4f} por llamada")
    print(f"[AHORRO] Con 1M llamadas/mes: ${savings_per_call * 1_000_000:.2f}/mes")


# ============================================================================
# EJEMPLO 2: Claude API Integration con archivos
# ============================================================================

def example_claude_integration():
    """
    Como usar TOONKIT con Claude API
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Anthropic Claude Integration")
    print("="*80)
    
    analytics_data = {
        "report_id": "report_2024_q1",
        "metrics": {
            "dau": 125000,
            "mau": 500000,
            "retention_d1": 0.65,
            "revenue": 2500000
        },
        "trends": [
            {"date": f"2024-03-{i+1:02d}", "value": 120000 + i*100} 
            for i in range(30)
        ]
    }
    
    json_str = json.dumps(analytics_data)
    toon_str = encode(analytics_data)
    
    print(f"\n[COMPARACION]")
    print(f"JSON: {len(json_str)} bytes")
    print(f"TOON: {len(toon_str)} bytes")
    print(f"Reduccion: {(1-len(toon_str)/len(json_str))*100:.1f}%")
    
    print(f"\n[CODIGO] Integracion con Claude:")
    print("""
import anthropic
from toonkit import encode

client = anthropic.Anthropic()

# Crear archivo con datos en formato TOON
analytics_toon = encode(analytics_data)

# Opcion 1: Enviar TOON como texto
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analiza estos datos (TOON):\\n{analytics_toon}"
    }]
)

# Opcion 2: Guardar archivo TOON y adjuntarlo
with open("analytics.toon", "w") as f:
    f.write(analytics_toon)

# Si usas Files API (beta):
# response = client.beta.files.upload(
#     file=("analytics.toon", analytics_toon),
# )

print(message.content[0].text)
""")


# ============================================================================
# EJEMPLO 3: Gemini Integration
# ============================================================================

def example_gemini_integration():
    """
    Como usar TOONKIT con Google Gemini
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Google Gemini Integration")
    print("="*80)
    
    # Conversacion larga
    conversation = {
        "user_profile": {
            "name": "Alice",
            "user_id": "user_789",
            "subscription": "premium"
        },
        "conversation_history": [
            {"role": "user", "content": "Como optimizo mis queries en PostgreSQL?"},
            {"role": "assistant", "content": "Aqui hay algunos tips..."},
            {"role": "user", "content": "Como uso indexes?"},
            {"role": "assistant", "content": "Los indexes aceleran queries..."},
            {"role": "user", "content": "Y transactions?"},
            {"role": "assistant", "content": "Las transactions aseguran..."}
        ] * 10  # Simulamos 60 mensajes
    }
    
    json_conv = json.dumps(conversation)
    toon_conv = encode(conversation)
    
    print(f"\n[DATOS GRANDES]")
    print(f"JSON: {len(json_conv):,} bytes ({len(json_conv)/4:.0f} tokens)")
    print(f"TOON: {len(toon_conv):,} bytes ({len(toon_conv)/4:.0f} tokens)")
    print(f"Reduccion: {(1-len(toon_conv)/len(json_conv))*100:.1f}%")
    
    print(f"\n[CODIGO] Integracion con Gemini:")
    print("""
import google.generativeai as genai
from toonkit import encode

genai.configure(api_key="YOUR_API_KEY")

# Convertir datos a TOON para contexto comprimido
context_toon = encode(conversation_data)

model = genai.GenerativeModel("gemini-pro")

# Multi-turn conversation con contexto TOON
response = model.generate_content([
    {
        "role": "user",
        "parts": [
            "Contexto (formato TOON comprimido):\\n" + context_toon,
            "\\nPregunta: Como puedo optimizar esto?"
        ]
    }
])

print(response.text)
""")


# ============================================================================
# EJEMPLO 4: Comparacion lado a lado
# ============================================================================

def example_comparison():
    """
    Comparacion practica de antes/despues
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Comparacion Practica - ANTES vs DESPUES")
    print("="*80)
    
    print("""
ESCENARIO: Sistema de CRM que envia contexto de cliente a Claude cada vez
que se abre un ticket de soporte. ~10,000 tickets/dia.

CALCULO CON LOS DATOS REALES:
""")
    
    # Datos reales
    large_context = {
        "customer_id": 12345,
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+34-600-123-456",
        "company": "TechCorp",
        "subscription_tier": "enterprise",
        "subscription_status": "active",
        "mrr": 5000,
        "arr": 60000,
        "payment_method": "credit_card",
        "billing_address": {
            "street": "Calle Principal 123",
            "city": "Madrid",
            "country": "Spain",
            "postal_code": "28001"
        },
        "shipping_address": {
            "street": "Avenida Secundaria 456",
            "city": "Barcelona",
            "country": "Spain",
            "postal_code": "08002"
        },
        "purchase_history": [
            {
                "order_id": f"ORD-{1000+i}",
                "date": f"2024-{(i%12)+1:02d}-{(i%28)+1:02d}",
                "items": [{"sku": f"PROD-{j}", "qty": j+1, "price": 100*j} for j in range(5)],
                "total": 1500+i*100,
                "status": "delivered" if i%2==0 else "processing"
            }
            for i in range(50)
        ],
        "support_tickets": [
            {
                "ticket_id": f"TKT-{5000+i}",
                "date": f"2024-03-{(i%27)+1:02d}",
                "subject": f"Issue {i}",
                "description": "Lorem ipsum dolor sit amet " * 10,
                "status": "resolved" if i%3==0 else "open",
                "resolution": "Fixed issue..." if i%3==0 else None,
                "response_time_hours": 2+i
            }
            for i in range(30)
        ],
        "preferences": {
            "language": "es",
            "timezone": "Europe/Madrid",
            "communication_preference": "email",
            "marketing_consent": True,
            "notifications_enabled": True
        },
        "usage_analytics": {
            "api_calls_this_month": 50000,
            "storage_used_gb": 250,
            "monthly_active_users": 15,
            "last_login": "2024-03-27T10:15:00Z"
        }
    }
    
    json_data = json.dumps(large_context)
    toon_data = encode(large_context)
    
    json_bytes = len(json_data)
    toon_bytes = len(toon_data)
    
    json_tokens = json_bytes / 4
    toon_tokens = toon_bytes / 4
    
    print(f"[TAMAÑO DEL CONTEXTO]")
    print(f"  JSON: {json_bytes:,} bytes ({json_tokens:.0f} tokens)")
    print(f"  TOON: {toon_bytes:,} bytes ({toon_tokens:.0f} tokens)")
    print(f"  Ahorro: {(1-toon_bytes/json_bytes)*100:.1f}%")
    
    print(f"\n[COSTOS DIARIOS]")
    tickets_per_day = 10000
    claude_rate = 0.015 / 1000  # $0.015 por 1k tokens
    
    json_cost_daily = json_tokens * claude_rate * tickets_per_day
    toon_cost_daily = toon_tokens * claude_rate * tickets_per_day
    daily_savings = json_cost_daily - toon_cost_daily
    
    print(f"  JSON: ${json_cost_daily:,.2f}/dia")
    print(f"  TOON: ${toon_cost_daily:,.2f}/dia")
    print(f"  Ahorro: ${daily_savings:,.2f}/dia")
    
    print(f"\n[PROYECCIONES ANUALES]")
    annual_savings = daily_savings * 365
    print(f"  Ahorro anual: ${annual_savings:,.2f}")
    print(f"  Ahorro 3 años: ${annual_savings * 3:,.2f}")
    print(f"  Ahorro 5 años: ${annual_savings * 5:,.2f}")
    
    print(f"\n[BENEFICIOS ADICIONALES]")
    print(f"  - Menor latencia de red")
    print(f"  - Mejor rendimiento de API")
    print(f"  - Escalabilidad mejorada")
    print(f"  - Huella de carbono reducida")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    example_openai_integration()
    example_claude_integration()
    example_gemini_integration()
    example_comparison()
    
    print("\n" + "="*80)
    print("FIN DE EJEMPLOS / END OF EXAMPLES")
    print("="*80)
    print("""
PROXIMO PASO / NEXT STEP:

1. Instala TOONKIT: pip install toonkit
2. Integra en tu codigo: from toonkit import encode, decode
3. Reemplaza json.dumps() con encode()
4. Reemplaza json.loads() con decode()
5. Observa los ahorros inmediatos!

SOPORTE / SUPPORT:
GitHub: https://github.com/cafep/toonkit
Issues: https://github.com/cafep/toonkit/issues
""")
