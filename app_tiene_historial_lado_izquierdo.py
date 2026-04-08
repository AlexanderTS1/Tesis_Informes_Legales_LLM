import streamlit as st
import os
import json
from datetime import datetime

from modules.ingestion.pdf_loader import guardar_pdf
from modules.extraction.text_extractor import extraer_texto_pdf
from modules.extraction.antecedentes import generar_antecedentes
from modules.legal.informe_legal import generar_informe_legal

# ================= CONFIG =================
UPLOAD_DIR = "data/uploads"
CONVERSATIONS_DIR = "data/conversations"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

st.set_page_config(
    page_title="OAJ - Asistente Jurídico Inteligente",
    layout="wide"
)

# ================= ESTILO CORPORATIVO =================
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }

    .stApp {
        background-color: #f4f6f9;
    }

    .css-1d391kg {
        background-color: #1f2b3a;
    }

    h1, h2, h3 {
        color: #1f2b3a;
    }
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "texto" not in st.session_state:
    st.session_state.texto = None

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# ================= FUNCIONES =================

def guardar_conversacion():
    if st.session_state.conversation_id:
        path = os.path.join(
            CONVERSATIONS_DIR,
            f"{st.session_state.conversation_id}.json"
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)


def cargar_conversacion(nombre_archivo):
    path = os.path.join(CONVERSATIONS_DIR, nombre_archivo)
    with open(path, "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)
    st.session_state.conversation_id = nombre_archivo.replace(".json", "")


def nueva_conversacion():
    st.session_state.messages = []
    st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")


# ================= SIDEBAR =================
with st.sidebar:
    st.title("📚 Expedientes y Conversaciones")

    # Nueva conversación
    if st.button("➕ Nueva conversación"):
        nueva_conversacion()

    st.markdown("### 🕘 Historial")

    conversaciones = os.listdir(CONVERSATIONS_DIR)

    for conv in sorted(conversaciones, reverse=True):
        if st.button(conv.replace(".json", ""), key=conv):
            cargar_conversacion(conv)

    st.markdown("---")

    st.markdown("### 📄 Cargar expediente")

    pdf_file = st.file_uploader("Subir PDF", type=["pdf"])

    if pdf_file:
        pdf_path = guardar_pdf(pdf_file)
        st.success("PDF cargado correctamente")

        if st.button("Procesar expediente"):
            with st.spinner("Extrayendo texto..."):
                st.session_state.texto = extraer_texto_pdf(pdf_path)
                st.session_state.pdf_loaded = True
                st.success("Expediente listo para consulta")

    st.markdown("---")
    st.info("Municipalidad Provincial de Calca\nOficina de Asesoría Jurídica")

# ================= HEADER =================
col1, col2 = st.columns([3, 1])

with col1:
    st.title("⚖️ Asistente Jurídico OAJ")

with col2:
    modelo = st.selectbox(
        "Modelo Jurídico",
        [
            "Modelo OAJ v1 (Recomendado)",
            "Modo Análisis",
            "Modo Redacción Formal"
        ]
    )

# ================= CHAT =================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escriba su consulta jurídica...")

if prompt:

    # Crear ID si no existe
    if not st.session_state.conversation_id:
        nueva_conversacion()

    # Mostrar usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ================= LÓGICA SEGÚN MODELO =================
    if not st.session_state.pdf_loaded:
        respuesta = "⚠️ Primero debe cargar y procesar un expediente."

    else:
        with st.spinner("Analizando expediente..."):

            if modelo == "Modo Análisis":
                respuesta = generar_antecedentes(st.session_state.texto)

            elif modelo == "Modo Redacción Formal":
                antecedentes = generar_antecedentes(st.session_state.texto)
                respuesta = generar_informe_legal(antecedentes)

            else:  # Modelo OAJ v1
                if "antecedente" in prompt.lower():
                    respuesta = generar_antecedentes(st.session_state.texto)

                elif "informe" in prompt.lower():
                    antecedentes = generar_antecedentes(st.session_state.texto)
                    respuesta = generar_informe_legal(antecedentes)

                else:
                    respuesta = generar_antecedentes(st.session_state.texto)

    # Mostrar respuesta
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    with st.chat_message("assistant"):
        st.markdown(respuesta)

    guardar_conversacion()
