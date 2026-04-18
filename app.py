import streamlit as st
import pandas as pd

# ===============================
# CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Trimetrix",
    layout="wide"
)

# ===============================
# ESTILO (FONDO OSCURO PRO)
# ===============================
st.markdown("""
<style>

/* Fondo */
.stApp {
    background: linear-gradient(135deg, #0F172A, #1E293B);
}

/* Tarjeta */
.block-container {
    padding: 40px;
}

/* Título */
h1 {
    color: white;
    font-size: 42px;
    font-weight: 600;
}

/* Labels */
label {
    color: #E2E8F0 !important;
}

/* Inputs */
.stSelectbox div {
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    color: white;
}

/* Slider */
.stSlider span {
    color: white !important;
}

/* Botón */
.stButton>button {
    background: linear-gradient(90deg, #00AEEF, #00D1B2);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# LAYOUT PRINCIPAL (CLAVE)
# ===============================
col_left, col_right = st.columns([1,3])

# 👉 LADO IZQUIERDO (ESPACIO PARA EL FONDO)
with col_left:
    st.markdown("")

# 👉 LADO DERECHO (FORMULARIO)
with col_right:

    st.markdown("# Trimetrix – Registro Clínico")

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

    # ===============================
    # LÓGICA CLÍNICA
    # ===============================
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

    # ===============================
    # GUARDAR
    # ===============================
    if st.button("Guardar registro clínico"):
        df = pd.DataFrame([data])
        df.to_csv("datos_trimetrix.csv", mode='a', header=False, index=False)
        st.success("Registro guardado correctamente")
