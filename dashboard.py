"""
Dashboard de Fundos de Investimento — ITAÚ EDITION 🧡💙
Design customizado para apresentação estratégica.
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
    page_title="Analytics Fundos — Itaú Vision",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════
# PALETA DE CORES OFICIAL (ITAÚ)
# ═══════════════════════════════════════════════════
ITA_LARANJA = "#FF6200"
ITA_LARANJA_SOFT = "#F88104"
ITA_AZUL_PROFUNDO = "#000B40"
ITA_AZUL_VIBRANTE = "#0520B7"
ITA_AZUL_CLARO = "#3B85FA"
ITA_VERDE = "#1F8102"
BACKGROUND_LIGHT = "#F4F5F7"
CARD_WHITE = "#FFFFFF"
TEXT_MAIN = "#1E1E1E"

ITA_PALETTE = [ITA_LARANJA, ITA_AZUL_VIBRANTE, "#FA9F09", "#02036C", ITA_VERDE, "#FBC305"]

# ═══════════════════════════════════════════════════
# CUSTOM CSS — ITAÚ UI/UX
# ═══════════════════════════════════════════════════
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {BACKGROUND_LIGHT};
    }}

    .stApp {{
        background-color: {BACKGROUND_LIGHT};
    }}

    /* Sidebar Custom */
    section[data-testid="stSidebar"] {{
        background-color: {ITA_AZUL_PROFUNDO} !important;
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
        border-left: 5px solid {ITA_LARANJA};
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
        color: {ITA_AZUL_PROFUNDO};
        font-size: 1.8rem;
        font-weight: 700;
    }}

    /* Tabs Custom */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px;
        color: {TEXT_MAIN};
        font-weight: 600;
        border-bottom: 2px solid transparent;
    }}
    .stTabs [aria-selected="true"] {{
        color: {ITA_LARANJA} !important;
        border-bottom: 2px solid {ITA_LARANJA} !important;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: {ITA_AZUL_PROFUNDO} !important;
        font-weight: 700 !important;
    }}

    /* Selectbox e inputs */
    .stSelectbox div[data-baseweb="select"] {{
        border-radius: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# FUNÇÃO AUXILIAR — CARDS
# ═══════════════════════════════════════════════════
def ita_metric(label, value):
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
    # Fallback se o arquivo não existir durante o desenvolvimento
    try:
        df = pd.read_csv(data_dir / "fundos_ativos.csv", encoding="utf-8-sig")
    except:
        # Mock de dados para não quebrar o layout no rebuild
        return pd.DataFrame({
            'denom_social': ['Fundo Exemplo Itaú'], 'classe': ['Renda Fixa'],
            'vl_patrim_liq': [1e9], 'idade_anos': [5], 'gestor': ['ITAÚ UNIBANCO'],
            'pl_milhoes': [1000], 'taxa_adm': [1.0], 'rentab_fundo': [12.5]
        })
    
    df["vl_patrim_liq"] = pd.to_numeric(df["vl_patrim_liq"], errors="coerce").fillna(0)
    df["taxa_adm"] = pd.to_numeric(df["taxa_adm"], errors="coerce")
    df["rentab_fundo"] = pd.to_numeric(df["rentab_fundo"], errors="coerce")
    df["idade_anos"] = pd.to_numeric(df["idade_anos"], errors="coerce").fillna(0)
    df["classe"] = df["classe"].fillna("Multimercado")
    df["gestor"] = df["gestor"].fillna("Não informado")
    df["pl_milhoes"] = df["vl_patrim_liq"] / 1e6
    return df

df = carregar_dados()
cdi_ref = 14.15

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Ita%C3%BA_Unibanco_logo.svg/512px-Ita%C3%BA_Unibanco_logo.svg.png", width=80)
    st.title("Asset Analytics")
    st.caption("Estratégia e Visão de Fundos")
    st.divider()
    
    classes = sorted(df["classe"].unique())
    classe_sel = st.multiselect("Filtrar Classe", classes, default=classes)
    
    pl_range = st.slider("PL (R$ Milhões)", 0, int(df["pl_milhoes"].max()), (0, int(df["pl_milhoes"].max())))
    
    st.divider()
    st.markdown("---")
    st.caption("Desenvolvido por Rodrigo Presida")

mask = (df["classe"].isin(classe_sel)) & (df["pl_milhoes"].between(pl_range[0], pl_range[1]))
df_filtrado = df[mask].copy()

# ═══════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════
st.title("Panorama de Mercado: Fundos de Investimento")
st.caption("Análise de competitividade, concentração e performance.")

col1, col2, col3, col4 = st.columns(4)
with col1: ita_metric("Total de Fundos", f"{len(df_filtrado):,}")
with col2: ita_metric("PL Total", f"R$ {df_filtrado['vl_patrim_liq'].sum()/1e9:.1f}B")
with col3: ita_metric("CDI Atual", f"{cdi_ref}%")
with col4: ita_metric("Idade Média", f"{df_filtrado['idade_anos'].mean():.1f} anos")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# DASHBOARD BODY
# ═══════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊 Visão de Mercado", "🏢 Análise de Gestores", "📋 Explorador de Dados"])

with tab1:
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Concentração por Classe")
        dist = df_filtrado["classe"].value_counts().reset_index()
        fig = px.bar(dist, x="count", y="index", orientation='h', 
                     color="count", color_continuous_scale=[[0, ITA_AZUL_PROFUNDO], [1, ITA_LARANJA]])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                          xaxis_title="Qtd Fundos", yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Distribuição de PL (Treemap)")
        pl_classe = df_filtrado.groupby("classe")["vl_patrim_liq"].sum().reset_index()
        fig = px.treemap(pl_classe, path=["classe"], values="vl_patrim_liq",
                         color="vl_patrim_liq", color_continuous_scale=[[0, ITA_AZUL_VIBRANTE], [1, ITA_LARANJA]])
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação Patrimônio vs Maturidade")
    fig = px.scatter(df_filtrado, x="idade_anos", y="pl_milhoes", color="classe", 
                     size="pl_milhoes", size_max=40, color_discrete_sequence=ITA_PALETTE)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Principais Players do Mercado")
    top_gestores = df_filtrado.groupby("gestor")["vl_patrim_liq"].sum().nlargest(10).reset_index()
    fig = px.bar(top_gestores, x="vl_patrim_liq", y="gestor", orientation='h',
                 color_discrete_sequence=[ITA_LARANJA])
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # HHI Index
    ms = df_filtrado["vl_patrim_liq"] / df_filtrado["vl_patrim_liq"].sum()
    hhi = (ms**2).sum() * 10000
    st.info(f"O Índice HHI do mercado filtrado é **{hhi:.0f}**. Isso indica um mercado {'Altamente Concentrado' if hhi > 2500 else 'Competitivo'}.")

with tab3:
    st.subheader("Base de Dados Estratégica")
    st.dataframe(df_filtrado[["denom_social", "gestor", "classe", "pl_milhoes", "rentab_fundo"]]
                 .sort_values("pl_milhoes", ascending=False), 
                 use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════
st.markdown(f"""
    <div style="text-align: center; color: {ITA_AZUL_PROFUNDO}; padding: 20px; font-size: 0.8rem;">
        Itaú Unibanco — Analytics Fundos | Dados CVM Maio 2026 | Rodrigo Presida
    </div>
""", unsafe_allow_html=True)
