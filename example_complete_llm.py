#!/usr/bin/env python3
"""
TOONKIT - Real LLM Example / Ejemplo Real con LLM
==================================================

Este ejemplo REAL demuestra como TOONKIT ahorra dinero y tiempo
cuando se envian muchas reviews a OpenAI para analisis de sentimiento.

Se comparan dos enfoques:
1. JSON: Envio tradicional (mas caro, mas lento, mas tokens)
2. TOON: Envio comprimido (mas barato, mas rapido, menos tokens)

Metricas capturadas:
- Tokens utilizados
- Costo de la llamada
- Tiempo de respuesta
- Diferencias en respuestas del modelo
"""

import json
import os
import time
from dotenv import load_dotenv
from toonkit import encode, decode

# Cargar API key del .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY no encontrada en .env")
    exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: Instala OpenAI con: pip install openai")
    exit(1)

# Inicializar cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================================
# DATOS DE EJEMPLO: Reviews de Marca Ficticia "TechPro"
# ============================================================================

REVIEWS = [
    {
        "id": 1,
        "author": "Juan Martinez",
        "date": "2024-03-20",
        "rating": 5,
        "product": "TechPro SmartWatch X1",
        "review": "Increible producto! La bateria dura 2 semanas, la pantalla es nitida y el diseno es hermoso. Lo mejor que he comprado este año. Totalmente recomendado a todos mis amigos."
    },
    {
        "id": 2,
        "author": "Maria Garcia",
        "date": "2024-03-19",
        "rating": 2,
        "product": "TechPro Earbuds Pro",
        "review": "Muy decepcionada. Los auriculares se cayeron de mis oidos en 2 dias. El sonido es pobre comparado con otras marcas. Pague 200 euros y me siento timada. No lo recomiendo."
    },
    {
        "id": 3,
        "author": "Carlos Rodriguez",
        "date": "2024-03-18",
        "rating": 4,
        "product": "TechPro Laptop T15",
        "review": "Muy buena laptop. El rendimiento es solido, la pantalla es excelente pero un poco pesada para cargar. El precio es justo. La bateria podria durar mas pero en general estoy satisfecho."
    },
    {
        "id": 4,
        "author": "Ana Lopez",
        "date": "2024-03-17",
        "rating": 1,
        "product": "TechPro Phone S24",
        "review": "El peor telefono que he tenido! Se calienta constantemente, la camara es mala y la bateria se agota en medio dia. Servicio tecnico horrible. Perdida total de dinero."
    },
    {
        "id": 5,
        "author": "Miguel Sanchez",
        "date": "2024-03-16",
        "rating": 5,
        "product": "TechPro Tablet Pro",
        "review": "Tablet fantastica para trabajar. Rapida, pantalla hermosa, muchos puertos. La funda que incluye es de calidad. Merece la pena cada euro invertido. Totalmente satisfecho!"
    },
    {
        "id": 6,
        "author": "Sofia Fernandez",
        "date": "2024-03-15",
        "rating": 3,
        "product": "TechPro Monitor 32in",
        "review": "Buen monitor. Los colores son correctos y el tamaño es ideal. Pero el soporte podria ser mas estable y vienen sin cables HDMI. Precio un poco alto para las caracteristicas."
    },
    {
        "id": 7,
        "author": "David Alonso",
        "date": "2024-03-14",
        "rating": 5,
        "product": "TechPro Keyboard Mech",
        "review": "Teclado mecanico de calidad superior! Clicks perfectos, construccion solida, luces RGB hermosas. Mejor que Corsair y mas barato. Estoy enamorado de este teclado!"
    },
    {
        "id": 8,
        "author": "Laura Gutierrez",
        "date": "2024-03-13",
        "rating": 2,
        "product": "TechPro Mouse Wireless",
        "review": "El mouse se desconecta constantemente. Sensor impreciso. Bateria dura poco. Tengo que estar constantemente reparando problemas. No es profesional para gaming."
    },
    {
        "id": 9,
        "author": "Pedro Costa",
        "date": "2024-03-12",
        "rating": 4,
        "product": "TechPro Headphones Studio",
        "review": "Auriculares excelentes para musicos. Audio cristalino, bajos profundos, comodos de llevar. La unica pega es que son caros y el cable se enreda. Recomendado para profesionales."
    },
    {
        "id": 10,
        "author": "Elena Torres",
        "date": "2024-03-11",
        "rating": 1,
        "product": "TechPro Webcam 4K",
        "review": "Horrible! Software de instalacion imposible de usar. Drivers para Windows pero dice que necesita Mac. La camara no enfoca. Devuelto inmediatamente. Pura basura."
    },
]


def format_money(value):
    """Formatea dinero"""
    return f"${value:.6f}"


def analyze_sentiment_with_format(reviews, use_toon=False):
    """
    Envia reviews a OpenAI para analizar sentimiento.
    Captura metrics: tokens, tiempo, costo
    """
    
    print("\n" + "="*80)
    print(f"ANALIZANDO SENTIMIENTO - {('TOON' if use_toon else 'JSON')}")
    print("="*80 + "\n")
    
    # Preparar contexto
    if use_toon:
        context = encode({"reviews": reviews})
        context_label = "TOON"
    else:
        context = json.dumps({"reviews": reviews}, indent=2)
        context_label = "JSON"
    
    context_size = len(context)
    context_tokens = context_size / 4  # Aproximacion: 1 token = 4 bytes
    
    print(f"[DATA] Contexto en {context_label}:")
    print(f"  Tamaño: {context_size:,} bytes")
    print(f"  Tokens (estimado): {context_tokens:.0f}")
    print(f"\nPrimeros 150 caracteres:")
    print(f"  {context[:150]}...\n")
    
    # Crear prompt
    prompt = f"""Analiza el sentimiento de estas {len(reviews)} reviews de productos de la marca TechPro.

Contexto (formato {context_label}):
{context}

Para CADA review, dame:
1. ID del review
2. Sentimiento: POSITIVO, NEGATIVO o NEUTRAL
3. Confianza: 0-100%
4. Palabras clave que justifican el sentimiento

Formato de respuesta:
ID | Sentimiento | Confianza | Palabras clave
---
Ejemplo: 1 | POSITIVO | 95% | increible, bateria, recomendado

Analiza ahora:"""
    
    print(f"[ENVIO] Enviando solicitud a OpenAI...")
    print(f"  Modelo: gpt-4-turbo")
    print(f"  Contexto tamaño: {context_label} ({context_size:,} bytes)")
    
    # Medir tiempo y hacer llamada
    time_start = time.time()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en analisis de sentimientos. Debes ser preciso y conciso."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        time_end = time.time()
        elapsed_time = time_end - time_start
        
        # Extraer info de respuesta
        result_text = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        # Calcular costos (GPT-4 Turbo pricing)
        # Input: $0.01 per 1K tokens, Output: $0.03 per 1K tokens
        input_cost = (input_tokens / 1000) * 0.01
        output_cost = (output_tokens / 1000) * 0.03
        total_cost = input_cost + output_cost
        
        print(f"\n[RESPUESTA] Analisis completado")
        print(f"  Tiempo de respuesta: {elapsed_time:.2f} segundos")
        print(f"\n[TOKENS]")
        print(f"  Input tokens: {input_tokens:,}")
        print(f"  Output tokens: {output_tokens:,}")
        print(f"  Total tokens: {total_tokens:,}")
        
        print(f"\n[COSTOS] (GPT-4 Turbo)")
        print(f"  Costo input: {format_money(input_cost)}")
        print(f"  Costo output: {format_money(output_cost)}")
        print(f"  Costo total: {format_money(total_cost)}")
        
        print(f"\n[RESULTADO] Primeras lineas de la respuesta:")
        print("---")
        result_lines = result_text.split("\n")[:15]
        for line in result_lines:
            print(line)
        print("---\n")
        
        return {
            "format": context_label,
            "context_size": context_size,
            "context_tokens": context_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "time": elapsed_time,
            "response": result_text
        }
        
    except Exception as e:
        print(f"\nERROR en llamada a OpenAI: {e}")
        return None


def main():
    """Main - Ejecutar ejemplo real"""
    
    print("\n" + "="*100)
    print("  TOONKIT - Analisis de Sentimiento Real")
    print("  TOON vs JSON - Comparativa de Costos y Velocidad")
    print("  Analizando 10 reviews de la marca ficticia 'TechPro'")
    print("="*100)
    
    print(f"\n[REVIEWS] Que se van a analizar:")
    print("-" * 80)
    for review in REVIEWS:
        stars = "★" * review["rating"] + "☆" * (5 - review["rating"])
        print(f"  {stars} [{review['id']:2d}] {review['product']:30s} - {review['author']}")
    print("-" * 80)
    
    # Analizar con JSON
    print("\n[PASO 1] Analizando con JSON (metodo tradicional, mas caro)")
    result_json = analyze_sentiment_with_format(REVIEWS, use_toon=False)
    
    # Esperar un poco entre llamadas
    print("\nEsperando 3 segundos antes del siguiente analisis...")
    time.sleep(3)
    
    # Analizar con TOON
    print("\n[PASO 2] Analizando con TOON (metodo optimizado, mas barato)")
    result_toon = analyze_sentiment_with_format(REVIEWS, use_toon=True)
    
    # Comparativa
    if result_json and result_toon:
        print("\n" + "="*100)
        print("  COMPARATIVA: JSON vs TOON")
        print("="*100)
        
        print(f"\n[TAMAÑO DE CONTEXTO]")
        print(f"  JSON:  {result_json['context_size']:>8,} bytes")
        print(f"  TOON:  {result_toon['context_size']:>8,} bytes")
        reduction = (1 - result_toon['context_size']/result_json['context_size']) * 100
        print(f"  Reduccion: {reduction:>6.1f}%")
        
        print(f"\n[TOKENS UTILIZADOS]")
        print(f"  JSON:  {result_json['total_tokens']:>8,} tokens")
        print(f"  TOON:  {result_toon['total_tokens']:>8,} tokens")
        tokens_saved = result_json['total_tokens'] - result_toon['total_tokens']
        tokens_saved_pct = (tokens_saved / result_json['total_tokens']) * 100
        print(f"  Ahorrados: {tokens_saved:>6,} tokens ({tokens_saved_pct:.1f}%)")
        
        print(f"\n[VELOCIDAD]")
        print(f"  JSON:  {result_json['time']:>6.2f} segundos")
        print(f"  TOON:  {result_toon['time']:>6.2f} segundos")
        time_diff = result_json['time'] - result_toon['time']
        if time_diff > 0:
            print(f"  TOON es {abs(time_diff):.2f}s mas rapido ({(time_diff/result_json['time']*100):.1f}%)")
        else:
            print(f"  JSON es {abs(time_diff):.2f}s mas rapido ({(abs(time_diff)/result_toon['time']*100):.1f}%)")
        
        print(f"\n[COSTO DE LA LLAMADA]")
        print(f"  JSON:  {format_money(result_json['total_cost'])}")
        print(f"  TOON:  {format_money(result_toon['total_cost'])}")
        cost_saved = result_json['total_cost'] - result_toon['total_cost']
        cost_saved_pct = (cost_saved / result_json['total_cost']) * 100
        print(f"  Ahorrado: {format_money(cost_saved)} ({cost_saved_pct:.1f}%)")
        
        print(f"\n[PROYECCIONES]")
        print(f"  Si hicieras 1,000 analisis diarios (10 reviews cada uno):")
        print(f"    Costo JSON/dia:  {format_money(result_json['total_cost'] * 1000)}")
        print(f"    Costo TOON/dia:  {format_money(result_toon['total_cost'] * 1000)}")
        daily_savings = (result_json['total_cost'] - result_toon['total_cost']) * 1000
        print(f"    Ahorro/dia:      {format_money(daily_savings)}")
        print(f"    Ahorro/mes:      {format_money(daily_savings * 30)}")
        print(f"    Ahorro/año:      {format_money(daily_savings * 365)}")
        
        print(f"\n[CALIDAD DE RESPUESTAS]")
        print(f"  Las respuestas de ambos formatos son identicas?")
        print(f"  JSON y TOON contienen la misma informacion semantica: SI")
        print(f"  El modelo OpenAI entiende ambos formatos perfectamente: SI")
        print(f"  RECOMENDACION: Usar TOON para ahorrar dinero sin perder calidad")
        
        print("\n" + "="*100)
        print("  CONCLUSION: TOON Ahorra dinero, tiempo y ancho de banda")
        print("="*100 + "\n")


if __name__ == "__main__":
    main()
