import streamlit as st
import pandas as pd
import base64

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Trimetrix", layout="wide")

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

/* TARJETA GLASS */
.form-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 40px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
}

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

</style>
""", unsafe_allow_html=True)

# ===============================
# LAYOUT
# ===============================
left, right = st.columns([1.2, 2])

with left:
    st.markdown(" ")  # espacio para ver frasco

with right:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

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

    if servicio == "Endodoncia":
        diagnostico = st.selectbox(
            "Diagnóstico",
            ["Pulpitis", "Necrosis", "Periodontitis apical"]
        )
        data["diagnostico"] = diagnostico

    uso = st.selectbox("¿Se indicó Trimetrix?", ["Sí", "No"])
    data["uso"] = uso

    if st.button("Guardar registro clínico"):
        df = pd.DataFrame([data])
        try:
            old = pd.read_csv("datos_trimetrix.csv")
            df = pd.concat([old, df], ignore_index=True)
        except:
            pass
        df.to_csv("datos_trimetrix.csv", index=False)
        st.success("Registro guardado correctamente")

    st.markdown('</div>', unsafe_allow_html=True)
