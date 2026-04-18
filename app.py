import streamlit as st
import pandas as pd
import base64

# 🔹 Fondo con imagen
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# 👉 usa tu imagen del frasco (sin ADN)
set_bg("fondo.png")


# 🔹 ESTILO PREMIUM TRANSPARENTE (GLASS)
st.markdown("""
<style>

/* Título */
h1 {
    color: white;
    text-align: center;
    font-size: 42px;
    font-weight: 600;
}

/* Tarjeta transparente */
.block-container {
    background: rgba(255, 255, 255, 0.08);  /* 🔥 súper transparente */
    backdrop-filter: blur(12px);            /* efecto vidrio */
    padding: 40px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Inputs */
.stSelectbox div, .stNumberInput div, .stTextInput div {
    background-color: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Texto */
label, .stSlider {
    color: white !important;
}

/* Botón premium */
.stButton>button {
    background: linear-gradient(90deg, #00AEEF, #00D1B2);
    color: white;
    border-radius: 12px;
    font-size: 16px;
    height: 50px;
    width: 100%;
    border: none;
}

/* Hover botón */
.stButton>button:hover {
    opacity: 0.9;
}

</style>
""", unsafe_allow_html=True)


# 🔹 TÍTULO
st.markdown("# Trimetrix – Registro Clínico")


# 🔹 FORMULARIO
servicio = st.selectbox(
    "Seleccione servicio",
    ["Endodoncia", "Periodoncia", "Cirugía oral", "Aftas", "Mucositis"]
)

col1, col2 = st.columns(2)

with col1:
    dolor = st.slider("Dolor (0-10)", 0, 10)

with col2:
    molestia = st.slider("Molestia oral (0-10)", 0, 10)

data = {
    "servicio": servicio,
    "dolor": dolor,
    "molestia": molestia
}

# 🔹 LÓGICA CLÍNICA
if servicio == "Aftas":
    lesiones = st.number_input("Número de lesiones", 1)
    data["lesiones"] = lesiones

if servicio == "Mucositis":
    grado = st.selectbox("Grado de mucositis", [0,1,2,3,4])
    data["grado"] = grado

if servicio == "Cirugía oral":
    procedimiento = st.selectbox("Tipo de procedimiento", ["Exodoncia", "Implante", "Otro"])
    data["procedimiento"] = procedimiento

if servicio == "Endodoncia":
    diagnostico = st.selectbox("Diagnóstico", ["Pulpitis", "Necrosis", "Periodontitis apical"])
    data["diagnostico"] = diagnostico

if servicio == "Periodoncia":
    sangrado = st.selectbox("Sangrado gingival", ["Ninguno", "Leve", "Moderado", "Severo"])
    data["sangrado"] = sangrado

uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
data["uso"] = uso


# 🔹 GUARDAR
if st.button("Guardar registro clínico"):
    df = pd.DataFrame([data])
    df.to_csv("datos_trimetrix.csv", mode='a', header=False, index=False)
    st.success("Registro guardado correctamente")
