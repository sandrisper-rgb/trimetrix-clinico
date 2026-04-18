import streamlit as st
import pandas as pd
import base64

# ===============================
# CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Trimetrix",
    layout="wide"
)

# ===============================
# FONDO CON IMAGEN + OVERLAY OSCURO
# ===============================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(5, 15, 35, 0.72), rgba(5, 15, 35, 0.72)),
            url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Asegúrate de tener la imagen subida al repo como fondo.png
set_bg("fondo.png")

# ===============================
# ESTILO PREMIUM
# ===============================
st.markdown("""
<style>

/* contenedor principal */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* título */
h1 {
    color: white;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
}

/* etiquetas */
label, .stMarkdown, p {
    color: #E5EEF8 !important;
    font-weight: 500;
}

/* cajas visuales */
[data-baseweb="select"] > div,
.stNumberInput > div > div,
.stTextInput > div > div {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* texto interno selects */
[data-baseweb="select"] * {
    color: white !important;
}

/* sliders */
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
    color: #DCE7F5 !important;
}

.stSlider span {
    color: #DCE7F5 !important;
}

/* botón */
.stButton > button {
    background: linear-gradient(90deg, #00AEEF, #10D6C2);
    color: white;
    border: none;
    border-radius: 14px;
    height: 3.2rem;
    width: 100%;
    font-size: 1.05rem;
    font-weight: 600;
}

.stButton > button:hover {
    opacity: 0.92;
}

/* mensaje de éxito */
.stSuccess {
    background: rgba(16, 214, 194, 0.12) !important;
    color: white !important;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LAYOUT: IZQUIERDA VACÍA, FORMULARIO A LA DERECHA
# ===============================
col_left, col_right = st.columns([1.2, 2.1])

with col_left:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    # vacío para dejar ver el frasco/fondo

with col_right:
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
        "molestia": molestia
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
        df = pd.DataFrame([data])
        try:
            old = pd.read_csv("datos_trimetrix.csv")
            df = pd.concat([old, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("datos_trimetrix.csv", index=False)
        st.success("Registro guardado correctamente")
