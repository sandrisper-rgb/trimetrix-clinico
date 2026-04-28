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
        data.get("causa_lesion", ""),
        data.get("tipo_lesion", ""),
        data.get("tamano_lesion_inicial", ""),
        data.get("diagnostico", ""),
        data.get("grado", ""),
        data.get("lesiones", ""),
        data.get("procedimiento", ""),
        data.get("sangrado", ""),
        data.get("uso", ""),
        data.get("frecuencia", ""),
        data.get("dias_uso", ""),
        data.get("dolor_dia1", ""),
        data.get("tamano_dia1", ""),
        data.get("dolor_dia3", ""),
        data.get("tamano_dia3", ""),
        data.get("dolor_dia7", ""),
        data.get("tamano_dia7", ""),
        data.get("dias_resolucion", ""),
        data.get("reaccion_adversa", "")
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

    # ===============================
    # DATOS DEL PROFESIONAL Y DEL CASO
    # ===============================
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

    # ===============================
    # EVALUACIÓN INICIAL
    # ===============================
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

    dolor_inicial = st.slider("Dolor inicial (0-10)", 0, 10)

    causa_lesion = st.text_area("Causa de la lesión")

    c1, c2 = st.columns(2)
    with c1:
        tipo_lesion = st.selectbox(
            "Tipo de lesión",
            ["Única", "Múltiple"]
        )
    with c2:
        tamano_lesion_inicial = st.selectbox(
            "Tamaño de la lesión",
            ["< a 2 mm", "> a 2 mm"]
        )

    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sede": sede,
        "odontologo": odontologo,
        "especialidad": especialidad,
        "codigo_paciente": codigo_paciente,
        "edad": edad,
        "servicio": servicio,
        "dolor_inicial": dolor_inicial,
        "causa_lesion": causa_lesion,
        "tipo_lesion": tipo_lesion,
        "tamano_lesion_inicial": tamano_lesion_inicial,
        "diagnostico": "",
        "grado": "",
        "lesiones": "",
        "procedimiento": "",
        "sangrado": "",
        "uso": "",
        "frecuencia": "",
        "dias_uso": "",
        "dolor_dia1": "",
        "tamano_dia1": "",
        "dolor_dia3": "",
        "tamano_dia3": "",
        "dolor_dia7": "",
        "tamano_dia7": "",
        "dias_resolucion": "",
        "reaccion_adversa": ""
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

    # ===============================
    # USO DE TRIMETRIX
    # ===============================
    st.markdown("### Uso de Trimetrix")

    uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
    data["uso"] = uso

    if uso == "Sí":
        c3, c4 = st.columns(2)

        with c3:
            frecuencia = st.selectbox(
                "Frecuencia de uso",
                ["1 vez/día", "2 veces/día"]
            )
        with c4:
            dias_uso = st.selectbox(
                "Días de uso",
                ["1", "3", "5", "7"]
            )

        data["frecuencia"] = frecuencia
        data["dias_uso"] = dias_uso

        # ===============================
        # SEGUIMIENTO
        # ===============================
        st.markdown("### Seguimiento con Trimetrix")

        st.markdown("#### Día 1")
        s1, s2 = st.columns(2)
        with s1:
            dolor_dia1 = st.slider("Dolor día 1 (0-10)", 0, 10)
        with s2:
            tamano_dia1 = st.selectbox(
                "Tamaño día 1",
                ["< a 2 mm", "> a 2 mm"]
            )

        st.markdown("#### Día 3")
        s3, s4 = st.columns(2)
        with s3:
            dolor_dia3 = st.slider("Dolor día 3 (0-10)", 0, 10)
        with s4:
            tamano_dia3 = st.selectbox(
                "Tamaño día 3",
                ["< a 2 mm", "> a 2 mm"]
            )

        st.markdown("#### Día 7")
        s5, s6 = st.columns(2)
        with s5:
            dolor_dia7 = st.slider("Dolor día 7 (0-10)", 0, 10)
        with s6:
            tamano_dia7 = st.selectbox(
                "Tamaño día 7",
                ["< a 2 mm", "> a 2 mm"]
            )

        # ===============================
        # EVALUACIÓN POSTERIOR
        # ===============================
        st.markdown("### Evaluación posterior al tratamiento")

        dias_resolucion = st.text_input(
            "¿En cuántos días se resolvió la lesión?"
        )

        reaccion_adversa = st.selectbox(
            "¿Presentó reacción adversa no deseada?",
            ["No", "Sí"]
        )

        data["dolor_dia1"] = dolor_dia1
        data["tamano_dia1"] = tamano_dia1
        data["dolor_dia3"] = dolor_dia3
        data["tamano_dia3"] = tamano_dia3
        data["dolor_dia7"] = dolor_dia7
        data["tamano_dia7"] = tamano_dia7
        data["dias_resolucion"] = dias_resolucion
        data["reaccion_adversa"] = reaccion_adversa

    if st.button("Guardar registro clínico"):
        try:
            guardar_en_sheets(data)
            st.success("Registro guardado correctamente en Google Sheets")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
