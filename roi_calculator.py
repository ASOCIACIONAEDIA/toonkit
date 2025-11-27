#!/usr/bin/env python3
"""
TOONKIT - ROI Calculator / Calculador de ROI

Calcula cuanto dinero tu empresa puede ahorrar usando TOONKIT
con tus propios datos y configuracion de LLM.

Uso:
    python roi_calculator.py

Luego sigue las instrucciones interactivas.
"""

import json
from toonkit import encode

def format_money(value):
    """Formatea valor a moneda"""
    return f"${value:,.2f}"

def get_user_input():
    """Obtiene datos del usuario de forma interactiva"""
    print("\n" + "="*80)
    print("TOONKIT - ROI Calculator / Calculador de ROI")
    print("="*80)
    
    print("\n[PASO 1] Describe tus datos de contexto")
    print("Pega un ejemplo de JSON que envias a tu LLM")
    print("(Termina con una línea vacía):\n")
    
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    json_str = "\n".join(lines)
    
    try:
        context_data = json.loads(json_str)
    except json.JSONDecodeError:
        print("\n❌ Error: JSON inválido. Intenta de nuevo.")
        return None
    
    print(f"\n✅ Datos parseados correctamente ({len(json_str)} bytes)")
    
    # Obtener configuración de LLM
    print("\n[PASO 2] Configuración de LLM")
    
    print("\nQue modelo de LLM usas? (escribe el número)")
    models = [
        {"id": 1, "name": "GPT-4 Turbo", "cost": 0.01, "desc": "$0.01 por 1K input tokens"},
        {"id": 2, "name": "GPT-3.5 Turbo", "cost": 0.0005, "desc": "$0.0005 por 1K input tokens"},
        {"id": 3, "name": "Claude 3 Opus", "cost": 0.015, "desc": "$0.015 por 1K input tokens"},
        {"id": 4, "name": "Claude 3 Sonnet", "cost": 0.003, "desc": "$0.003 por 1K input tokens"},
        {"id": 5, "name": "Gemini Pro", "cost": 0.00025, "desc": "$0.00025 por 1K input tokens"},
        {"id": 6, "name": "Personalizado", "cost": None, "desc": "Especificar costo custom"},
    ]
    
    for m in models:
        print(f"  {m['id']}. {m['name']} ({m['desc']})")
    
    choice = input("\nNumero (1-6): ").strip()
    
    try:
        choice = int(choice)
        if choice < 1 or choice > 6:
            print("❌ Opcion invalida")
            return None
        
        selected_model = models[choice - 1]
        
        if choice == 6:
            cost_str = input("Especifica el costo por 1K tokens (ej: 0.01): ").strip()
            selected_model["cost"] = float(cost_str)
            selected_model["name"] = input("Nombre del modelo (ej: mi-llm): ").strip()
    except (ValueError, IndexError):
        print("❌ Error en la seleccion")
        return None
    
    # Obtener volumen de llamadas
    print(f"\n✅ Modelo seleccionado: {selected_model['name']}")
    
    print("\n[PASO 3] Volumen de llamadas")
    
    volume_str = input("Cuantas llamadas por mes? (ej: 100000): ").strip()
    
    try:
        monthly_calls = int(volume_str)
    except ValueError:
        print("❌ Numero invalido")
        return None
    
    return {
        "context": context_data,
        "json_str": json_str,
        "model": selected_model,
        "monthly_calls": monthly_calls
    }


def calculate_roi(data):
    """Calcula el ROI basado en los datos del usuario"""
    
    print("\n" + "="*80)
    print("CALCULANDO ROI...")
    print("="*80)
    
    context = data["context"]
    json_str = data["json_str"]
    model = data["model"]
    monthly_calls = data["monthly_calls"]
    
    # Calcular tamaños
    json_bytes = len(json_str)
    toon_str = encode(context)
    toon_bytes = len(toon_str)
    
    reduction_pct = (1 - toon_bytes/json_bytes) * 100
    
    # Calcular tokens
    json_tokens = json_bytes / 4
    toon_tokens = toon_bytes / 4
    tokens_saved_per_call = json_tokens - toon_tokens
    
    # Calcular costos
    json_cost_per_call = json_tokens / 1000 * model["cost"]
    toon_cost_per_call = toon_tokens / 1000 * model["cost"]
    savings_per_call = json_cost_per_call - toon_cost_per_call
    
    # Proyecciones
    annual_calls = monthly_calls * 12
    monthly_savings = savings_per_call * monthly_calls
    annual_savings = savings_per_call * annual_calls
    
    # ROI
    implementation_cost = 5000  # Costo tipico de implementacion
    payback_months = implementation_cost / monthly_savings if monthly_savings > 0 else float('inf')
    roi_pct = (annual_savings / implementation_cost * 100) if implementation_cost > 0 else 0
    
    # Mostrar resultados
    print("\n[RESULTADOS]")
    print("-" * 80)
    
    print(f"\n📊 COMPRESSION:")
    print(f"  JSON:  {json_bytes:,} bytes ({json_tokens:.0f} tokens)")
    print(f"  TOON:  {toon_bytes:,} bytes ({toon_tokens:.0f} tokens)")
    print(f"  Reduccion: {reduction_pct:.1f}%")
    print(f"  Tokens ahorrados por llamada: {tokens_saved_per_call:.0f}")
    
    print(f"\n💰 COSTOS POR LLAMADA:")
    print(f"  JSON: {format_money(json_cost_per_call)}")
    print(f"  TOON: {format_money(toon_cost_per_call)}")
    print(f"  Ahorro: {format_money(savings_per_call)}")
    
    print(f"\n📈 PROYECCIONES:")
    print(f"  Llamadas/mes: {monthly_calls:,}")
    print(f"  Llamadas/año: {annual_calls:,}")
    print(f"  Ahorro mensual: {format_money(monthly_savings)}")
    print(f"  Ahorro anual: {format_money(annual_savings)}")
    print(f"  Ahorro 3 años: {format_money(annual_savings * 3)}")
    print(f"  Ahorro 5 años: {format_money(annual_savings * 5)}")
    
    print(f"\n🎯 ROI:")
    print(f"  Costo implementacion: {format_money(implementation_cost)}")
    if payback_months != float('inf'):
        print(f"  Periodo de amortizacion: {payback_months:.1f} meses")
        print(f"  ROI anual: {roi_pct:.0f}%")
    else:
        print(f"  No hay ahorros suficientes para amortizar")
    
    print("\n" + "-" * 80)
    
    # Recomendación
    print("\n[RECOMENDACION]")
    if reduction_pct < 5:
        print("⚠️  La reducción es pequeña. TOONKIT podría no ser necesario para este caso.")
    elif payback_months > 12:
        print("⚠️  El periodo de amortización es largo (>12 meses). Considera si vale la pena.")
    elif payback_months > 6:
        print("✅ Buena oportunidad. ROI en ~6-12 meses.")
    elif payback_months > 2:
        print("✅ Muy buena oportunidad. ROI rápido en 2-6 meses.")
    else:
        print("🚀 Excelente oportunidad. ROI MUY rápido (<2 meses). Implementar ahora!")
    
    print("\n" + "="*80)


def main():
    """Main"""
    try:
        data = get_user_input()
        if data:
            calculate_roi(data)
        else:
            print("\n❌ Abortado")
    except KeyboardInterrupt:
        print("\n\nAbortado por usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
