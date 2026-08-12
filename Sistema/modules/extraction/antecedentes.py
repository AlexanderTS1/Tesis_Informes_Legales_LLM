#✅ extracción estructurada de ANTECEDENTES

#✅ Plan and Solve + Chain of Verification

#✅ coherente con una tesis (variables, nombres, metodología)
import os
import json
import random
import time
import re
import requests

# ================= CONFIGURACIÓN =================
ENTRENAMIENTO_PATH = "/content/drive/MyDrive/Analisis/Entrenamiento.txt"
RESULTADOS_DIR = "/content/drive/MyDrive/resultados"

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = "apikey"
CLAUDE_API_VERSION = "2023-06-01"

MODELO = "CLAUDE"
PROMPT_STRATEGY = "PLAN_AND_SOLVE + CHAIN_OF_VERIFICATION"

# ================= ARCHIVOS =================
def seleccionar_archivo_aleatorio():
    if not os.path.exists(ENTRENAMIENTO_PATH):
        print("No se encontró el archivo de entrenamiento.")
        return None

    rutas_validas = []
    with open(ENTRENAMIENTO_PATH, "r", encoding="utf-8") as f:
        for linea in f:
            path = linea.strip()
            if path.endswith(".txt") and os.path.exists(path):
                rutas_validas.append(path)

    return random.choice(rutas_validas) if rutas_validas else None


def leer_archivo(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ================= CLAUDE =================
def llamar_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": CLAUDE_API_VERSION,
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(CLAUDE_API_URL, json=payload, headers=headers)
    if r.status_code != 200:
        print("Error Claude:", r.text)
        return ""

    return r.json()["content"][0]["text"].strip()


# ================= PROMPT ANTECEDENTES =================
PROMPT_ANTECEDENTES = """
Actúa como abogado especialista en asesoría jurídica administrativa.

OBJETIVO:
Extraer y organizar los ANTECEDENTES relevantes de un expediente administrativo
a partir de los actuados contenidos en el texto.

FASE 1 – IDENTIFICACIÓN:
Identifica informes, oficios, memorandos, resoluciones u otros documentos relevantes.

FASE 2 – EXTRACCIÓN:
Para cada documento identificado, extrae:
- Tipo de documento
- Número
- Oficina de origen
- Oficina de destino
- Asunto
- Fecha
- Descripción objetiva

FASE 3 – ORGANIZACIÓN:
Ordena los antecedentes cronológicamente y redáctalos en lenguaje técnico-jurídico,
formal e impersonal.

REGLAS:
- No resumas ni interpretes.
- No inventes información.
- Mantén fidelidad documental.
"""

def generar_antecedentes(texto):
    return llamar_claude(f"{PROMPT_ANTECEDENTES}\n\nTexto administrativo:\n{texto}")

# ================= VERIFICACIÓN =================
def verificar_antecedentes(texto_original, antecedentes):
    prompt = f"""
Verifica los antecedentes extraídos a partir del texto original.

1. Detecta errores o inconsistencias.
2. Identifica omisiones relevantes.
3. Evalúa fidelidad documental.

Finaliza con el formato EXACTO:
Puntuación: X/5

Texto original:
{texto_original}

Antecedentes extraídos:
{antecedentes}
"""
    return llamar_claude(prompt)

# ================= GUARDAR =================
def guardar_resultados_json(archivo, antecedentes, verificacion):
    data = {
        "id": os.path.basename(archivo),
        "modelo": MODELO,
        "estrategia": PROMPT_STRATEGY,
        "antecedentes_generados": antecedentes,
        "verificacion": verificacion
    }

    carpeta = os.path.join(RESULTADOS_DIR, "antecedentes", MODELO)
    os.makedirs(carpeta, exist_ok=True)

    path = os.path.join(carpeta, os.path.basename(archivo).replace(".txt", ".json"))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Resultados guardados en:", path)

# ================= MAIN =================
def main():
    archivo = seleccionar_archivo_aleatorio()
    if not archivo:
        print("No se pudo seleccionar archivo.")
        return

    texto = leer_archivo(archivo)
    if not texto:
        print("No se pudo leer el expediente.")
        return

    antecedentes = generar_antecedentes(texto)
    time.sleep(30)

    verificacion = verificar_antecedentes(texto, antecedentes)

    guardar_resultados_json(archivo, antecedentes, verificacion)

# ================= RUN =================
if __name__ == "__main__":
    main()
