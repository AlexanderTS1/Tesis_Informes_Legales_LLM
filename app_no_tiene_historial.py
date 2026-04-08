'''import streamlit as st
import os
from modules.ingestion.pdf_loader import guardar_pdf
from modules.extraction.text_extractor import extraer_texto_pdf
from modules.extraction.antecedentes import generar_antecedentes
from modules.legal.informe_legal import generar_informe_legal

# ================= CONFIG =================
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="Sistema de Informes Legales - OAJ",
    layout="wide"
)

# Inicializar estados
if "texto" not in st.session_state:
    st.session_state.texto = None

if "antecedentes" not in st.session_state:
    st.session_state.antecedentes = None

if "informe" not in st.session_state:
    st.session_state.informe = None

# ================= UI =================
st.title("📑 Sistema Inteligente de Informes Legales")
st.subheader("Municipalidad Provincial de Calca – Oficina de Asesoría Jurídica")

st.markdown("---")

# ================= CARGA PDF =================
st.header("1️⃣ Carga del expediente administrativo")

pdf_file = st.file_uploader(
    "Seleccione el expediente en formato PDF",
    type=["pdf"]
)

if pdf_file:
    pdf_path = guardar_pdf(pdf_file)
    st.success("📄 PDF cargado correctamente")

    # ================= EXTRACCIÓN TEXTO =================
    st.header("2️⃣ Extracción de texto del expediente")

    if st.button("🔍 Extraer texto"):
        with st.spinner("Extrayendo texto del expediente..."):
            st.session_state.texto = extraer_texto_pdf(pdf_path)

    if st.session_state.texto:
        st.success("✅ Texto extraído correctamente")
        st.text_area("Texto del expediente", st.session_state.texto, height=250)

    # ================= ANTECEDENTES =================
    st.header("3️⃣ Extracción de antecedentes")

    if st.button("📌 Generar antecedentes") and st.session_state.texto:
        with st.spinner("Analizando actuados..."):
            st.session_state.antecedentes = generar_antecedentes(st.session_state.texto)

    if st.session_state.antecedentes:
        st.success("✅ Antecedentes generados")
        st.text_area("Antecedentes", st.session_state.antecedentes, height=300)

    # ================= INFORME LEGAL =================
    st.header("4️⃣ Generación del informe legal")

    if st.button("⚖️ Generar informe legal") and st.session_state.antecedentes:
        with st.spinner("Redactando informe legal..."):
            st.session_state.informe = generar_informe_legal(st.session_state.antecedentes)

    if st.session_state.informe:
        st.success("📘 Informe legal generado")
        st.text_area("Informe Legal", st.session_state.informe, height=400)'''
        

import streamlit as st
import os
from modules.ingestion.pdf_loader import guardar_pdf
from modules.extraction.text_extractor import extraer_texto_pdf
from modules.extraction.antecedentes import generar_antecedentes
from modules.legal.informe_legal import generar_informe_legal

# ================= CONFIG =================
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="OAJ - Asistente Legal Inteligente",
    layout="wide"
)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "texto" not in st.session_state:
    st.session_state.texto = None

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# ================= SIDEBAR =================
with st.sidebar:
    st.title("📚 Expediente")

    pdf_file = st.file_uploader(
        "Cargar expediente PDF",
        type=["pdf"]
    )

    if pdf_file:
        pdf_path = guardar_pdf(pdf_file)
        st.success("PDF cargado")

        if st.button("Procesar expediente"):
            with st.spinner("Extrayendo texto..."):
                st.session_state.texto = extraer_texto_pdf(pdf_path)
                st.session_state.pdf_loaded = True
                st.success("Expediente listo para consulta")

    st.markdown("---")
    st.info("Sistema Inteligente de Informes Legales\nMunicipalidad Provincial de Calca")

# ================= MAIN =================
st.title("⚖️ Asistente Jurídico OAJ")

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
prompt = st.chat_input("Escriba su consulta jurídica...")

if prompt:
    # Mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Procesar consulta
    if not st.session_state.pdf_loaded:
        respuesta = "⚠️ Primero debe cargar y procesar un expediente."
    else:
        with st.spinner("Analizando..."):

            if "antecedente" in prompt.lower():
                respuesta = generar_antecedentes(st.session_state.texto)

            elif "informe" in prompt.lower():
                antecedentes = generar_antecedentes(st.session_state.texto)
                respuesta = generar_informe_legal(antecedentes)

            elif "resumen" in prompt.lower():
                respuesta = generar_antecedentes(st.session_state.texto)

            else:
                respuesta = "Consulta recibida. Puede solicitar antecedentes, informe legal o resumen del expediente."

    # Mostrar respuesta
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    with st.chat_message("assistant"):
        st.markdown(respuesta)


