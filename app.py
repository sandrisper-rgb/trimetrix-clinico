import streamlit as st
import base64
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Trimetrix", layout="wide")

# ===============================
# GOOGLE SHEETS
# ===============================
def conectar_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    return client.open("Trimetrix_Clinico").sheet1

def guardar(data):
    sheet = conectar_sheet()
    sheet.append_row(list(data.values()))

# ===============================
# FONDO
# ===============================
def set_bg(img):
    with open(img, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
        linear-gradient(rgba(5,15,35,0.65), rgba(5,15,35,0.65)),
        url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("fondo.png")

# ===============================
# UI
# ===============================
st.title("Trimetrix – Registro Clínico")

# ===== DATOS =====
st.subheader("Datos del profesional")

c1, c2, c3 = st.columns(3)
with c1:
    sede = st.selectbox("Sede", ["Toberín", "Otra"])
with c2:
    odontologo = st.text_input("Odontólogo")
with c3:
    edad = st.number_input("Edad", 0, 120)

# ===== INICIAL =====
st.subheader("Evaluación inicial")

dolor = st.slider("Dolor inicial", 0, 10)

causa = st.text_area("Causa de la lesión")

tipo_lesion = st.selectbox(
    "Tipo de lesión",
    ["Única", "Múltiple"]
)

tamano = st.selectbox(
    "Tamaño de la lesión",
    ["<2mm", ">2mm"]
)

# ===== USO =====
st.subheader("Uso de Trimetrix")

uso = st.selectbox("¿Se indicó?", ["Sí", "No"])

frecuencia = st.selectbox(
    "Frecuencia",
    ["1 vez/día", "2 veces/día"]
)

dias = st.selectbox(
    "Días de uso",
    ["1", "3", "5", "7"]
)

# ===== SEGUIMIENTO =====
if uso == "Sí":
    st.subheader("Seguimiento")

    st.markdown("Día 1")
    d1_dolor = st.slider("Dolor día 1", 0, 10)
    d1_tamano = st.selectbox("Tamaño día 1", ["<2mm", ">2mm"])

    st.markdown("Día 3")
    d3_dolor = st.slider("Dolor día 3", 0, 10)
    d3_tamano = st.selectbox("Tamaño día 3", ["<2mm", ">2mm"])

    st.markdown("Día 7")
    d7_dolor = st.slider("Dolor día 7", 0, 10)
    d7_tamano = st.selectbox("Tamaño día 7", ["<2mm", ">2mm"])

    resolucion = st.text_input("¿En cuántos días se resolvió?")

    adversa = st.selectbox(
        "¿Reacción adversa?",
        ["Sí", "No"]
    )

# ===== GUARDAR =====
if st.button("Guardar registro"):
    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sede": sede,
        "odontologo": odontologo,
        "edad": edad,
        "dolor_inicial": dolor,
        "causa": causa,
        "tipo_lesion": tipo_lesion,
        "tamano": tamano,
        "uso": uso,
        "frecuencia": frecuencia,
        "dias": dias,
        "d1_dolor": d1_dolor if uso=="Sí" else "",
        "d1_tamano": d1_tamano if uso=="Sí" else "",
        "d3_dolor": d3_dolor if uso=="Sí" else "",
        "d3_tamano": d3_tamano if uso=="Sí" else "",
        "d7_dolor": d7_dolor if uso=="Sí" else "",
        "d7_tamano": d7_tamano if uso=="Sí" else "",
        "resolucion": resolucion if uso=="Sí" else "",
        "adversa": adversa if uso=="Sí" else ""
    }

    guardar(data)
    st.success("Guardado correctamente")
