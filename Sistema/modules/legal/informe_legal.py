#script para informe legal
import os
import json
import time
import requests

# ================= CONFIGURACIÓN =================
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = "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"
CLAUDE_API_VERSION = "2023-06-01"

MODELO = "CLAUDE"
PROMPT_STRATEGY = "PLAN_AND_SOLVE + CHAIN_OF_VERIFICATION"

# ================= CLAUDE =================
def llamar_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": CLAUDE_API_VERSION,
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(CLAUDE_API_URL, json=payload, headers=headers)
    if r.status_code != 200:
        print("Error Claude:", r.text)
        return ""

    return r.json()["content"][0]["text"].strip()
# ================= PROMPTS =================
PROMPT_BASE_LEGAL = """
Actúa como abogado especialista en Derecho Administrativo peruano,
con amplia experiencia en la elaboración de informes legales institucionales
en el sector público.

OBJETIVO:
Elaborar exclusivamente la sección II. BASE LEGAL de un informe legal,
limitándote a IDENTIFICAR y LISTAR las normas jurídicas aplicables,
utilizando únicamente los ANTECEDENTES proporcionados en formato JSON
y conforme al ordenamiento jurídico vigente en el Perú.

FASE 1 – PLANIFICACIÓN (Plan and Solve):
A partir de los antecedentes, identifica internamente la naturaleza
jurídico-administrativa del caso (por ejemplo: obra pública, inversión
pública, contratación estatal, gestión administrativa, modificación
presupuestal, ampliación de plazo u otros).
Esta identificación es solo para orientar la selección normativa y
NO debe ser incluida en la respuesta.

FASE 2 – SELECCIÓN NORMATIVA:
Determina únicamente las normas pertinentes al caso identificado,
priorizando:
- Constitución Política del Perú (solo si resulta aplicable)
- Leyes y Decretos Legislativos
- Reglamentos
- Directivas, resoluciones o disposiciones administrativas vigentes

FASE 3 – REDACCIÓN DE LA BASE LEGAL:
Redacta la sección II. BASE LEGAL LIMITÁNDOTE EXCLUSIVAMENTE a:
- Listar las normas aplicables
- Indicar el nombre completo de la norma
- Señalar su número y año de promulgación (cuando corresponda)

NO debes:
- Explicar el contenido de las normas
- Describir artículos
- Relacionar normas con los antecedentes
- Realizar análisis, interpretaciones ni conclusiones

CHAIN OF VERIFICATION (Verificación obligatoria antes de responder):
- Verifica que todas las normas citadas existan en el ordenamiento jurídico peruano.
- Verifica que las normas estén vigentes o sean aplicables al caso.
- Elimina cualquier norma irrelevante o no sustentada en los antecedentes.
- Asegura que no se haya incluido ninguna descripción normativa.

REGLAS ESTRICTAS:
- No inventes normas, artículos ni disposiciones.
- No incluyas artículos ni incisos.
- No utilices frases explicativas.
- Usa lenguaje técnico-jurídico, formal e impersonal.
- Redacta en formato institucional.

FORMATO DE SALIDA OBLIGATORIO:

II. BASE LEGAL

- [Listado enumerado o con viñetas de normas jurídicas]
"""
PROMPT_ANALISIS = """
Actúa como abogado especialista en Derecho Administrativo peruano,
con experiencia en la elaboración de informes legales institucionales
en entidades públicas.

OBJETIVO:
Desarrollar exclusivamente la sección III. ANÁLISIS de un informe legal,
evaluando jurídicamente los hechos contenidos en los ANTECEDENTES,
aplicando de manera estricta la BASE LEGAL previamente determinada.

FASE 1 – PLANIFICACIÓN (Plan and Solve):
Identifica internamente los problemas jurídicos relevantes que se
desprenden de los antecedentes administrativos, considerando la
naturaleza del caso (obra pública, inversión pública, contratación
estatal, ampliación de plazo, modificación presupuestal, procedimiento
administrativo u otros).
Esta identificación es solo para estructurar el análisis y NO debe ser
incluida en la respuesta.

BASE LEGAL (uso obligatorio y exclusivo):
- Constitución Política del Perú
- Ley Orgánica de Municipalidades – Ley N° 27972
- Ley del Procedimiento Administrativo General – Ley N° 27444
- Normas específicas del caso previamente determinadas

FASE 2 – DESARROLLO DEL ANÁLISIS:
Redacta el análisis jurídico aplicando exclusivamente las normas
contenidas en la BASE LEGAL, evaluando su aplicación a los hechos
descritos en los antecedentes.

Cada párrafo del análisis debe:
- Iniciar obligatoriamente con la expresión: “Que,”
- Desarrollar un razonamiento jurídico claro y coherente
- Vincular los hechos administrativos con la norma aplicable
- Mantener un enfoque descriptivo-argumentativo sin emitir conclusiones

CHAIN OF VERIFICATION (verificación previa obligatoria):
- Verifica que cada argumento esté sustentado en los antecedentes.
- Verifica que todas las normas aplicadas estén incluidas en la BASE LEGAL.
- Elimina cualquier análisis no respaldado normativamente.
- Confirma que ningún párrafo contenga conclusiones o recomendaciones.
- Confirma que todos los párrafos inicien con “Que,”.

REGLAS ESTRICTAS:
- No inventes hechos, documentos ni actuaciones administrativas.
- No incorpores normas distintas a las señaladas en la BASE LEGAL.
- No adelantes conclusiones finales ni recomendaciones.
- Usa lenguaje técnico-jurídico formal, impersonal e institucional.
- Redacta en estilo propio de informes legales del sector público.

FORMATO DE SALIDA OBLIGATORIO:

III. ANÁLISIS

Que, ............................................................
Que, ............................................................
Que, ............................................................
"""
PROMPT_CONCLUSIONES = """
Actúa como abogado especialista en Derecho Administrativo peruano,
con experiencia en la elaboración de informes legales institucionales
en entidades públicas.

OBJETIVO:
Redactar exclusivaOmente la sección IV. CNCLUSIONES del informe legal,
formulando conclusiones jurídicas que se desprendan de manera directa,
lógica y coherente del ANÁLISIS previamente desarrollado.

FASE 1 – PLANIFICACIÓN (Plan and Solve):
Identifica internamente las ideas jurídicas finales que resultan del
análisis, sin incorporar nuevos hechos, normas ni argumentos distintos
a los ya evaluados.
Esta fase es únicamente para organizar las conclusiones y NO debe ser
incluida en la respuesta.

FASE 2 – FORMULACIÓN DE CONCLUSIONES:
Redacta conclusiones jurídicas que:
- Sinteticen los resultados del análisis
- Determinen la situación jurídica del caso
- Precisen la viabilidad legal del procedimiento o actuación evaluada

CHAIN OF VERIFICATION (verificación previa obligatoria):
- Verifica que cada conclusión tenga sustento directo en el análisis.
- Elimina cualquier conclusión que introduzca hechos nuevos.
- Elimina cualquier referencia normativa no tratada en el análisis.
- Verifica que no existan recomendaciones explícitas ni implícitas.
- Asegura que no se repita el desarrollo argumentativo del análisis.

REGLAS ESTRICTAS:
- No introduzcas nuevos hechos, documentos ni actuaciones administrativas.
- No incorpores normas distintas a las ya analizadas.
- No formules recomendaciones ni propuestas de actuación.
- No repitas ni desarrolles nuevamente el análisis jurídico.
- Usa lenguaje técnico-jurídico formal, impersonal e institucional.

FORMATO DE SALIDA OBLIGATORIO:

IV. CONCLUSIONES

1. ............................................................
2. ............................................................
3. ............................................................
"""
PROMPT_RECOMENDACIONES = """
Actúa como abogado especialista en Derecho Administrativo peruano,
con experiencia en asesoría legal institucional en entidades públicas
y en prevención de responsabilidad administrativa, civil y penal
de funcionarios y servidores públicos.

OBJETIVO:
Redactar exclusivamente la sección V. RECOMENDACIONES del informe legal,
formulando recomendaciones técnicas, concretas y jurídicamente viables,
dirigidas a las oficinas, gerencias o unidades orgánicas competentes,
con la finalidad de:

- Garantizar el cumplimiento del ordenamiento jurídico vigente.
- Prevenir la configuración de infracciones administrativas.
- Evitar posibles responsabilidades civiles o penales.
- Asegurar actuaciones conforme a los principios de legalidad,
  razonabilidad, debido procedimiento y control interno.

Las recomendaciones deben guardar coherencia estricta con las
CONCLUSIONES previamente desarrolladas y con la Base Legal aplicada.

FASE 1 – PLANIFICACIÓN INTERNA (Plan and Solve):
- Identifica las conclusiones relevantes.
- Determina los riesgos jurídicos derivados de dichas conclusiones.
- Define qué órgano es competente para adoptar cada acción.
- Establece medidas preventivas o correctivas proporcionales.

Esta fase es únicamente interna y NO debe aparecer en la respuesta.

FASE 2 – FORMULACIÓN DE RECOMENDACIONES:

Redacta recomendaciones que:

- Se deriven directa y exclusivamente de las conclusiones.
- Estén dirigidas expresamente al órgano competente.
- Establezcan acciones concretas, claras y ejecutables.
- Incorporen medidas de prevención de riesgos legales.
- Promuevan el respeto a la legalidad y al debido procedimiento.
- Eviten vacíos que puedan generar nulidad o responsabilidad funcional.

CADENA DE VERIFICACIÓN (Chain of Verification):

Antes de emitir la respuesta, verifica que:

- Cada recomendación tenga sustento explícito en una conclusión.
- No se incorporen hechos, normas o argumentos nuevos.
- No se repitan análisis jurídicos previos.
- No existan contradicciones con la Base Legal aplicada.
- No se formulen recomendaciones genéricas o ambiguas.
- Todas las recomendaciones inicien obligatoriamente con:
  “Se recomienda”.

REGLAS ESTRICTAS:

- No introduzcas nuevas normas no analizadas.
- No amplíes el marco fáctico.
- No formules advertencias alarmistas sin sustento en las conclusiones.
- Usa lenguaje técnico-jurídico formal, impersonal e institucional.
- No menciones la fase de planificación ni la verificación interna.

FORMATO DE SALIDA OBLIGATORIO:

V. RECOMENDACIONES

1. Se recomienda a la [Oficina / Gerencia / Unidad Orgánica competente], adoptar las acciones administrativas necesarias a fin de ........................................, garantizando el cumplimiento de ........................................ y evitando la eventual configuración de responsabilidades funcionales.

2. Se recomienda a la [Oficina / Gerencia / Unidad Orgánica competente], disponer ........................................, conforme a las conclusiones expuestas, asegurando la observancia de los principios de legalidad y debido procedimiento administrativo.
"""
PROMPT_JURISPRUDENCIA="""
Actúa como especialista en Derecho Administrativo y redacción de opiniones legales en el sector público peruano.
Redacta exclusivamente el apartado de Jurisprudencia aplicable, identificando y desarrollando precedentes similares al caso planteado

METODOLOGÍA:
Aplicar PLAN AND SOLVE + CHAIN OF VERIFICATION.

OBJETIVO:
Generar únicamente el apartado:
"VI. JURISPRUDENCIA APLICABLE"

ENTRADA:
{descripcion_del_caso}

FASE 1 – PLAN:
- Identificar problema jurídico central.
- Identificar principios administrativos involucrados.

FASE 2 – SOLVE:
- Seleccionar jurisprudencia del TC, Corte Suprema, OSCE y Contraloría.
- Desarrollar:
   • Número de expediente
   • Criterio jurídico
   • Principio desarrollado
   • Aplicación concreta

FASE 3 – VERIFICACIÓN:
- Confirmar coherencia normativa.
- Confirmar pertinencia al caso.
- Eliminar precedentes dudosos.
- Evitar contradicciones legales.

FORMATO DE SALIDA:

VI. JURISPRUDENCIA APLICABLE

6.1 Tribunal Constitucional
6.2 Corte Suprema
6.3 Tribunal de Contrataciones del Estado
6.4 Contraloría
6.5 Aplicación Integrada al Caso """

PROMPT_INFORME_LEGAL = f"""
Actúa como abogado especialista en derecho administrativo peruano,
Considerar que eres jefe de la oficina de asesoria juridica con experiencia en elaboración de informes legales institucionales
en entidades públicas.

OBJETIVO GENERAL:
Elaborar un INFORME LEGAL profesional y completo, utilizando
exclusivamente la información contenida en los ANTECEDENTES
proporcionados en formato JSON, conforme al ordenamiento jurídico del Perú.

Iniciar el Infome legal con la siguiente Frase Mediante el presente me dirijo a
Ud. en atención al Informe de la referencia mediante el cual se solicita
Pronunciamiento Legal sobre "indicar el asunto del opinion legal".

====================================================
ESTRUCTURA OBLIGATORIA DEL INFORME LEGAL
====================================================

I. ANTECEDENTES
Redacta los antecedentes de forma cronológica, objetiva y clara,
utilizando únicamente la información contenida en el JSON.
No realices análisis ni interpretaciones jurídicas.

----------------------------------------------------

II. BASE LEGAL
Aplica estrictamente las siguientes instrucciones:
{PROMPT_BASE_LEGAL}

----------------------------------------------------

III. ANÁLISIS
Aplica estrictamente las siguientes instrucciones:
{PROMPT_ANALISIS}

----------------------------------------------------

IV. CONCLUSIONES
Aplica estrictamente las siguientes instrucciones:
{PROMPT_CONCLUSIONES}

----------------------------------------------------

V. RECOMENDACIONES
Aplica estrictamente las siguientes instrucciones:
{PROMPT_RECOMENDACIONES}

VI. JURISPRUDENCIA
Aplica estrictamente las siguientes instrucciones:
{PROMPT_JURISPRUDENCIA}

====================================================
REGLAS GENERALES OBLIGATORIAS
====================================================

- Usa lenguaje técnico-jurídico formal, impersonal e institucional.
- No inventes hechos, documentos ni normas.
- No introduzcas normativa no contenida en la Base Legal.
- No muestres razonamiento interno paso a paso.
- Mantén coherencia lógica entre todas las secciones.
- Si la información es insuficiente para alguna sección,
  indícalo expresamente en dicha sección.

====================================================
INSUMO ÚNICO AUTORIZADO
====================================================

ANTECEDENTES (JSON):
{{json_antecedentes}}
"""

def generar_informe_legal(antecedentes_json, jurisdiccion="Perú"):
    prompt = f"""
{PROMPT_INFORME_LEGAL}

Jurisdicción aplicable: {jurisdiccion}

ANTECEDENTES (JSON):
{json.dumps(antecedentes_json, indent=2, ensure_ascii=False)}
"""
    return llamar_claude(prompt)

# ================= VERIFICACIÓN =================
def verificar_informe(informe):
    prompt = f"""
Verifica el siguiente informe legal.

1. Coherencia jurídica
2. Correcta aplicación normativa
3. Consistencia entre antecedentes, análisis y conclusión

Finaliza con el formato EXACTO:
Puntuación: X/5

Informe legal:
{informe}
"""
    return llamar_claude(prompt)

