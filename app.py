import streamlit as st
import base64
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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
        data.get("fecha", ""),
        data.get("sede", ""),
        data.get("odontologo", ""),
        data.get("especialidad", ""),
        data.get("codigo_paciente", ""),
        data.get("edad", ""),
        data.get("servicio", ""),
        data.get("dolor_inicial", ""),
        data.get("molestia_inicial", ""),
        data.get("diagnostico", ""),
        data.get("grado", ""),
        data.get("lesiones", ""),
        data.get("procedimiento", ""),
        data.get("sangrado", ""),
        data.get("uso", ""),
        data.get("frecuencia", ""),
        data.get("dias_uso", ""),
        data.get("dolor_posterior", ""),
        data.get("molestia_posterior", ""),
        data.get("mejoria", ""),
        data.get("tolerancia", ""),
        data.get("observaciones", ""),
        data.get("lo_usaria_nuevamente", "")
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
# ESTILO
# ===============================
st.markdown("""
<style>
h1 {
    color: white;
    font-size: 2.8rem;
    font-weight: 700;
}

h3 {
    color: #EAF2FF;
    margin-top: 1rem;
}

label {
    color: #EAF2FF !important;
}

[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 12px;
    color: white !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.10) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.10) !important;
    color: white !important;
    border-radius: 12px !important;
}

textarea {
    background: rgba(255,255,255,0.10) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stSlider span {
    color: white !important;
}

.stButton>button {
    background: linear-gradient(90deg,#00AEEF,#00D1B2);
    color: white;
    border-radius: 14px;
    height: 50px;
    width: 100%;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    opacity: 0.9;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LAYOUT
# ===============================
left, right = st.columns([1.1, 2.1])

with left:
    st.markdown(" ")

with right:
    st.markdown("# Trimetrix – Registro Clínico")

    st.markdown("### Datos del profesional y del caso")

    c0_1, c0_2 = st.columns(2)
    with c0_1:
        sede = st.selectbox(
            "Sede",
            ["Toberín", "Otra sede"]
        )
    with c0_2:
        especialidad = st.selectbox(
            "Especialidad",
            [
                "Odontología general",
                "Endodoncia",
                "Periodoncia",
                "Cirugía oral",
                "Ortodoncia",
                "Odontopediatría",
                "Medicina oral"
            ]
        )

    c0_3, c0_4, c0_5 = st.columns(3)
    with c0_3:
        odontologo = st.text_input("Nombre del odontólogo")
    with c0_4:
        codigo_paciente = st.text_input("Código del paciente")
    with c0_5:
        edad = st.number_input("Edad del paciente", min_value=0, max_value=120, step=1)

    st.markdown("### Evaluación inicial")

    servicio = st.selectbox(
        "Seleccione servicio",
        [
            "Odontología general",
            "Endodoncia",
            "Periodoncia",
            "Cirugía oral",
            "Ortodoncia",
            "Odontopediatría",
            "Aftas",
            "Mucositis"
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        dolor_inicial = st.slider("Dolor inicial (0-10)", 0, 10)
    with c2:
        molestia_inicial = st.slider("Molestia oral inicial (0-10)", 0, 10)

    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sede": sede,
        "odontologo": odontologo,
        "especialidad": especialidad,
        "codigo_paciente": codigo_paciente,
        "edad": edad,
        "servicio": servicio,
        "dolor_inicial": dolor_inicial,
        "molestia_inicial": molestia_inicial,
        "diagnostico": "",
        "grado": "",
        "lesiones": "",
        "procedimiento": "",
        "sangrado": "",
        "uso": "",
        "frecuencia": "",
        "dias_uso": "",
        "dolor_posterior": "",
        "molestia_posterior": "",
        "mejoria": "",
        "tolerancia": "",
        "observaciones": "",
        "lo_usaria_nuevamente": ""
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

    if servicio == "Ortodoncia":
        procedimiento = st.selectbox(
            "Tipo de caso ortodóncico",
            ["Control", "Inicio tratamiento", "Ajuste", "Urgencia"]
        )
        data["procedimiento"] = procedimiento

    if servicio == "Odontopediatría":
        diagnostico = st.selectbox(
            "Motivo de consulta",
            ["Caries", "Dolor", "Control", "Trauma", "Infección"]
        )
        data["diagnostico"] = diagnostico

    st.markdown("### Uso de Trimetrix")

    c3, c4, c5 = st.columns(3)
    with c3:
        uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
    with c4:
        frecuencia = st.selectbox(
            "Frecuencia de uso",
            ["1 vez/día", "2 veces/día", "3 veces/día"]
        )
    with c5:
        dias_uso = st.selectbox(
            "Días de uso",
            ["1", "3", "5", "7", "10", "14"]
        )

    data["uso"] = uso
    data["frecuencia"] = frecuencia
    data["dias_uso"] = dias_uso

    if uso == "Sí":
        st.markdown("### Evaluación posterior al tratamiento")

        c6, c7 = st.columns(2)
        with c6:
            dolor_posterior = st.slider("Dolor posterior (0-10)", 0, 10)
        with c7:
            molestia_posterior = st.slider("Molestia oral posterior (0-10)", 0, 10)

        c8, c9 = st.columns(2)
        with c8:
            mejoria = st.selectbox("¿El paciente mejoró?", ["Sí", "Parcial", "No"])
        with c9:
            tolerancia = st.selectbox("Tolerancia al producto", ["Buena", "Regular", "Mala"])

        observaciones = st.text_area("Observaciones clínicas postratamiento")
        lo_usaria_nuevamente = st.selectbox("¿Lo usaría nuevamente?", ["Sí", "No"])

        data["dolor_posterior"] = dolor_posterior
        data["molestia_posterior"] = molestia_posterior
        data["mejoria"] = mejoria
        data["tolerancia"] = tolerancia
        data["observaciones"] = observaciones
        data["lo_usaria_nuevamente"] = lo_usaria_nuevamente

    if st.button("Guardar registro clínico"):
        try:
            guardar_en_sheets(data)
            st.success("Registro guardado correctamente en Google Sheets")
        except Exception as e:
            st.error(f"Error al guardar: {e}")

