import streamlit as st
import json
import os
import requests
import time
from datetime import datetime

# ── Página ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GeoJSON Highway Generator",
    page_icon="🗺️",
    layout="centered",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stButton > button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 0;
        font-size: 1rem;
    }
    .stButton > button:hover { background-color: #1D4ED8; }
    .result-box {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Rodovias ──────────────────────────────────────────────────────────────────
RODOVIAS_REAIS = [
    "Rodovia BR-101, Rio de Janeiro, Brasil",
    "Rodovia BR-116 Presidente Dutra, São Paulo, Brasil",
    "Rodovia BR-040, Belo Horizonte, Minas Gerais, Brasil",
    "Rodovia BR-060, Brasília, Distrito Federal, Brasil",
    "Rodovia BR-153 Belém-Brasília, Goiânia, Goiás, Brasil",
]

# ── Geocodificação ────────────────────────────────────────────────────────────
_cache_geocode: dict = {}

def geocodificar_endereco(endereco: str, api_key: str) -> tuple[float, float] | None:
    if endereco in _cache_geocode:
        return _cache_geocode[endereco]
    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": endereco, "key": api_key, "region": "br", "language": "pt-BR"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "OK":
            loc = data["results"][0]["geometry"]["location"]
            resultado = (loc["lng"], loc["lat"])
            _cache_geocode[endereco] = resultado
            return resultado
        st.warning(f"Sem resultado para `{endereco}`: **{data.get('status')}**")
    except requests.RequestException as e:
        st.error(f"Erro de rede: {e}")
    _cache_geocode[endereco] = None
    return None

# ── Interface ─────────────────────────────────────────────────────────────────
st.title("GeoJSON Highway Generator")
st.caption("Geocodifica as 5 rodovias de referência e exporta um GeoJSON pronto para uso.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Configurações")
    api_key = st.text_input(
        "Google Cloud API Key",
        value=os.environ.get("GOOGLE_API_KEY", ""),
        type="password",
        placeholder="AIza...",
    )
    pasta_saida = st.text_input("Pasta de saída", value="output")

with col2:
    st.subheader("Rodovias")
    for rodovia in RODOVIAS_REAIS:
        st.markdown(f"- {rodovia}")

st.divider()

executar = st.button("▶ Geocodificar e Gerar GeoJSON")

if executar:
    if not api_key.strip():
        st.error("Informe a Google API Key antes de continuar.")
        st.stop()

    progress_bar = st.progress(0)
    status_text = st.empty()
    features = []
    total = len(RODOVIAS_REAIS)

    for i, rodovia in enumerate(RODOVIAS_REAIS):
        status_text.text(f"Geocodificando {i + 1} de {total} — {rodovia}")
        coords = [0.0, 0.0]
        resultado = geocodificar_endereco(rodovia, api_key.strip())
        if resultado:
            coords = list(resultado)
        time.sleep(0.05)

        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {
                "id": i + 1,
                "rodovia": rodovia,
                "data_processamento": datetime.now().strftime("%Y-%m-%d"),
            },
        })
        progress_bar.progress((i + 1) / total)

    status_text.empty()
    progress_bar.empty()

    geojson = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:4674"}},
        "metadata": {
            "schema_version": "1.0",
            "ano_referencia": 2026,
            "data_geracao": datetime.now().isoformat(),
        },
        "features": features,
    }

    os.makedirs(pasta_saida, exist_ok=True)
    caminho_json = os.path.join(pasta_saida, "saida_artesp.geojson")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    st.markdown(f"""
    <div class="result-box">
        <strong>Concluído!</strong><br>
        <strong>{total}</strong> rodovias georreferenciadas.<br>
        Salvo em: <code>{os.path.abspath(caminho_json)}</code>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Download")
    st.download_button(
        label="Baixar GeoJSON",
        data=json.dumps(geojson, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="saida_artesp.geojson",
        mime="application/geo+json",
    )

    with st.expander("Visualizar GeoJSON", expanded=False):
        st.json(geojson)
