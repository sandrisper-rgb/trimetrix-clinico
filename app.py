import streamlit as st
import pandas as pd

st.title("Registro Clínico Trimetrix")

# Selección de servicio
servicio = st.selectbox(
    "Seleccione servicio",
    ["Endodoncia", "Periodoncia", "Cirugía oral", "Aftas", "Mucositis"]
)

# Síntomas
dolor = st.slider("Dolor (0-10)", 0, 10)
ardor = st.slider("Ardor (0-10)", 0, 10)
molestia = st.slider("Molestia oral (0-10)", 0, 10)

data = {
    "servicio": servicio,
    "dolor": dolor,
    "ardor": ardor,
    "molestia": molestia
}

# Lógica por servicio
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

# Uso del producto
uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
data["uso"] = uso

# Guardar datos
if st.button("Guardar"):
    df = pd.DataFrame([data])
    df.to_csv("datos_trimetrix.csv", mode='a', header=False, index=False)
    st.success("Registro guardado correctamente")
