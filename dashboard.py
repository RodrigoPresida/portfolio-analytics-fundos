"""
Dashboard de Fundos de Investimento — Analytics Pro 📊
Design de alto impacto visual focado em Data Storytelling.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="Asset Analytics — Rodrigo Presida",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════
# PALETA DE CORES — IMPACTO (VIBRANTE)
# ═══════════════════════════════════════════════════
COLOR_BRAND = "#FF6200"     # Laranja Principal
COLOR_NAVY = "#000B40"      # Azul Marinho Profundo
COLOR_BLUE = "#0520B7"      # Azul Vibrante
COLOR_GOLD = "#FA9F09"      # Ouro
BACKGROUND_PAGE = "#F4F5F7"
CARD_WHITE = "#FFFFFF"
TEXT_DARK = "#1E1E1E"

VIBRANT_PALETTE = [COLOR_BRAND, COLOR_BLUE, COLOR_GOLD, "#02036C", "#1F8102", "#FBC305"]

# ═══════════════════════════════════════════════════
# CUSTOM CSS — PREMIUM UI/UX
# ═══════════════════════════════════════════════════
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {BACKGROUND_PAGE};
    }}

    /* Sidebar Custom */
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_NAVY} !important;
        color: white !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {{
        color: white !important;
    }}

    /* Custom Metric Cards */
    .metric-card {{
        background-color: {CARD_WHITE};
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid {COLOR_BRAND};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }}
    .metric-label {{
        color: #6B7280;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}
    .metric-value {{
        color: {COLOR_NAVY};
        font-size: 1.8rem;
        font-weight: 700;
    }}

    /* Tabs Custom */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
        color: #64748B;
    }}
    .stTabs [aria-selected="true"] {{
        color: {COLOR_BRAND} !important;
        border-bottom: 2px solid {COLOR_BRAND} !important;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: {COLOR_NAVY} !important;
        font-weight: 700 !important;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# FUNÇÃO AUXILIAR — CARDS
# ═══════════════════════════════════════════════════
def custom_metric(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# CARREGAR DADOS
# ═══════════════════════════════════════════════════
@st.cache_data
def carregar_dados():
    data_dir = Path(__file__).parent / "data"
    try:
        df = pd.read_csv(data_dir / "fundos_ativos.csv", encoding="utf-8-sig")
    except:
        return pd.DataFrame({
            'denom_social': ['Fundo Exemplo'], 'classe': ['Renda Fixa'],
            'vl_patrim_liq': [1e9], 'idade_anos': [5], 'gestor': ['Gestora Global'],
            'pl_milhoes': [1000], 'taxa_adm': [1.0], 'rentab_fundo': [12.5]
        })
    
    df["vl_patrim_liq"] = pd.to_numeric(df["vl_patrim_liq"], errors="coerce").fillna(0)
    df["idade_anos"] = pd.to_numeric(df["idade_anos"], errors="coerce").fillna(0)
    df["classe"] = df["classe"].fillna("Outros")
    df["gestor"] = df["gestor"].fillna("Não informado")
    df["pl_milhoes"] = df["vl_patrim_liq"] / 1e6
    return df

df = carregar_dados()

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.title("Asset Analytics")
    st.caption("Visão Estratégica de Mercado")
    st.divider()
    
    classes = sorted(df["classe"].unique())
    classe_sel = st.multiselect("Classes de Ativos", classes, default=classes)
    
    pl_range = st.slider("PL (R$ Milhões)", 0, int(df["pl_milhoes"].max()), (0, int(df["pl_milhoes"].max())))
    
    st.divider()
    st.caption("Engenharia de Dados por Rodrigo Presida")

mask = (df["classe"].isin(classe_sel)) & (df["pl_milhoes"].between(pl_range[0], pl_range[1]))
df_filtrado = df[mask].copy()

# ═══════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════
st.title("Panorama de Mercado: Fundos de Investimento")
st.caption("Exploração quantitativa de ativos e concentração de mercado.")

col1, col2, col3, col4 = st.columns(4)
with col1: custom_metric("Total de Fundos", f"{len(df_filtrado):,}")
with col2: custom_metric("PL Total", f"R$ {df_filtrado['vl_patrim_liq'].sum()/1e9:.1f}B")
with col3: custom_metric("CDI Atual", "14.15%")
with col4: custom_metric("Idade Média", f"{df_filtrado['idade_anos'].mean():.1f} anos")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# DASHBOARD BODY
# ═══════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊 Inteligência de Mercado", "🏢 Análise de Players", "📋 Base de Dados"])

with tab1:
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Concentração por Classe")
        dist = df_filtrado["classe"].value_counts().reset_index()
        dist.columns = ["Classe", "Quantidade"]
        fig = px.bar(dist, x="Quantidade", y="Classe", orientation='h', 
                     color="Quantidade", color_continuous_scale=[[0, COLOR_NAVY], [1, COLOR_BRAND]])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Nº de Fundos", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Distribuição de Patrimônio")
        pl_classe = df_filtrado.groupby("classe")["vl_patrim_liq"].sum().reset_index()
        fig = px.treemap(pl_classe, path=["classe"], values="vl_patrim_liq",
                         color="vl_patrim_liq", color_continuous_scale=[[0, COLOR_BLUE], [1, COLOR_BRAND]])
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação Patrimônio vs Maturidade do Fundo")
    fig = px.scatter(df_filtrado, x="idade_anos", y="pl_milhoes", color="classe", 
                     size="pl_milhoes", size_max=40, color_discrete_sequence=VIBRANT_PALETTE)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Top 10 Gestores por Patrimônio Líquido")
    top_gestores = df_filtrado.groupby("gestor")["vl_patrim_liq"].sum().nlargest(10).reset_index()
    fig = px.bar(top_gestores, x="vl_patrim_liq", y="gestor", orientation='h', color_discrete_sequence=[COLOR_BRAND])
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Patrimônio Total")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Explorador de Dados Brutos")
    st.dataframe(df_filtrado[["denom_social", "gestor", "classe", "pl_milhoes"]]
                 .sort_values("pl_milhoes", ascending=False), 
                 use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════
st.markdown(f"""
    <div style="text-align: center; color: {COLOR_NAVY}; padding: 20px; font-size: 0.8rem; font-weight: 600;">
        Portfolio Rodrigo Presida | Análise de Ativos Financeiros | {datetime.now().year}
    </div>
""", unsafe_allow_html=True)
