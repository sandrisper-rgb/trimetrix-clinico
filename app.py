import streamlit as st
import pandas as pd
import base64
import gspread
from google.oauth2.service_account import Credentials

# ===============================
# CONFIG
# ===============================
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
    sheet = client.open("Trimetrix_Clinico").sheet1
    return sheet

def guardar_en_sheets(data):
    sheet = conectar_sheet()
    sheet.append_row([
        data.get("servicio", ""),
        data.get("dolor", ""),
        data.get("molestia", ""),
        data.get("diagnostico", ""),
        data.get("grado", ""),
        data.get("lesiones", ""),
        data.get("procedimiento", ""),
        data.get("sangrado", ""),
        data.get("uso", "")
    ])

# ===============================
# FONDO
# ===============================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(5,15,35,0.60), rgba(5,15,35,0.60)),
            url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("fondo.png")

# ===============================
# ESTILO PREMIUM
# ===============================
st.markdown("""
<style>

/* TÍTULO */
h1 {
    color: white;
    font-size: 2.8rem;
    font-weight: 700;
}

/* LABELS */
label {
    color: #EAF2FF !important;
}

/* INPUTS */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 12px;
    color: white !important;
}

/* SLIDER */
.stSlider span {
    color: white !important;
}

/* BOTÓN */
.stButton>button {
    background: linear-gradient(90deg,#00AEEF,#00D1B2);
    color: white;
    border-radius: 14px;
    height: 50px;
    width: 100%;
    border: none;
    font-weight: 600;
}

/* BOTÓN HOVER */
.stButton>button:hover {
    opacity: 0.9;
}

/* Espaciado general */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LAYOUT
# ===============================
left, right = st.columns([1.2, 2])

with left:
    st.markdown(" ")

with right:
    st.markdown("# Trimetrix – Registro Clínico")

    servicio = st.selectbox(
        "Seleccione servicio",
        ["Endodoncia", "Periodoncia", "Cirugía oral", "Aftas", "Mucositis"]
    )

    c1, c2 = st.columns(2)

    with c1:
        dolor = st.slider("Dolor (0-10)", 0, 10)

    with c2:
        molestia = st.slider("Molestia oral (0-10)", 0, 10)

    data = {
        "servicio": servicio,
        "dolor": dolor,
        "molestia": molestia,
        "diagnostico": "",
        "grado": "",
        "lesiones": "",
        "procedimiento": "",
        "sangrado": "",
        "uso": ""
    }

    if servicio == "Aftas":
        lesiones = st.number_input("Número de lesiones", min_value=1, step=1)
        data["lesiones"] = lesiones

    if servicio == "Mucositis":
        grado = st.selectbox("Grado de mucositis", [0, 1, 2, 3, 4])
        data["grado"] = grado

    if servicio == "Cirugía oral":
        procedimiento = st.selectbox(
            "Tipo de procedimiento",
            ["Exodoncia", "Implante", "Otro"]
        )
        data["procedimiento"] = procedimiento

    if servicio == "Endodoncia":
        diagnostico = st.selectbox(
            "Diagnóstico",
            ["Pulpitis", "Necrosis", "Periodontitis apical"]
        )
        data["diagnostico"] = diagnostico

    if servicio == "Periodoncia":
        sangrado = st.selectbox(
            "Sangrado gingival",
            ["Ninguno", "Leve", "Moderado", "Severo"]
        )
        data["sangrado"] = sangrado

    uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
    data["uso"] = uso

    if st.button("Guardar registro clínico"):
        try:
            guardar_en_sheets(data)
            st.success("Registro guardado correctamente en Google Sheets")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
