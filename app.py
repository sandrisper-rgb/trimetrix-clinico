import streamlit as st
import pandas as pd
import base64

# 🔹 Función para poner fondo con imagen
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

# 👉 IMPORTANTE: sube la imagen a GitHub como "fondo.png"
set_bg("fondo.png")

# 🔹 Estilo premium
st.markdown("""
<style>
/* Título */
h1 {
    color: #00AEEF;
    text-align: center;
    font-size: 40px;
}

/* Tarjetas */
.block-container {
    background: rgba(15, 23, 42, 0.85);
    padding: 30px;
    border-radius: 15px;
}

/* Botón */
.stButton>button {
    background: linear-gradient(90deg, #00AEEF, #00D1B2);
    color: white;
    border-radius: 10px;
    font-size: 16px;
    height: 50px;
    width: 100%;
}

/* Texto */
label, .stSelectbox, .stSlider {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🔹 Título
st.markdown("# 🧬 Trimetrix – Registro Clínico")

# 🔹 Formulario
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

# 🔹 Lógica clínica
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

# 🔹 Guardar
if st.button("Guardar registro clínico"):
    df = pd.DataFrame([data])
    df.to_csv("datos_trimetrix.csv", mode='a', header=False, index=False)
    st.success("Registro guardado correctamente")
