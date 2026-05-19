"""
Dashboard de Fundos de Investimento — Stack AWS
Dados reais da CVM (maio/2026). Paleta Itaú. Streamlit + Plotly.
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
    page_title="Fundos BR — Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════
# PALETA ITAÚ
# ═══════════════════════════════════════════════════
ITAU_LARANJA = "#EC7000"
ITAU_AZUL_ESCURO = "#003087"
ITAU_AZUL_CLARO = "#106EB0"
ITAU_CINZA = "#5C5C5C"
BACKGROUND = "#080c14"
CARD_BG = "#111827"
TEXT_PRIMARY = "#F9FAFB"
TEXT_MUTED = "#9CA3AF"

PALETTE = [
    "#EC7000",  # laranja Itaú
    "#106EB0",  # azul claro
    "#003087",  # azul escuro
    "#2CA02C",  # verde
    "#8E44AD",  # roxo
    "#E74C3C",  # vermelho
    "#F39C12",  # amarelo
    "#1ABC9C",  # teal
]
acessivel = px.colors.sequential.Viridis

# ═══════════════════════════════════════════════════
# CSS INJETADO (OVERLAY ESCURO)
# ═══════════════════════════════════════════════════
st.markdown(f"""
<style>
    .stApp {{
        background-color: {BACKGROUND};
    }}
    .stMetric {{
        background-color: {CARD_BG} !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }}
    .stMetric label {{
        color: {TEXT_MUTED} !important;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {ITAU_LARANJA} !important;
        font-size: 2rem !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #0d1320 !important;
        border-right: 1px solid #1e293b !important;
    }}
    .stSelectbox label, .stSlider label {{
        color: {TEXT_MUTED} !important;
    }}
    h1, h2, h3 {{
        color: {TEXT_PRIMARY} !important;
    }}
    p, span, div {{
        color: {TEXT_PRIMARY};
    }}
    .stDataFrame {{
        background-color: {CARD_BG} !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# CARREGAR DADOS
# ═══════════════════════════════════════════════════
@st.cache_data
def carregar_dados():
    data_dir = Path(__file__).parent / "data"
    df = pd.read_csv(data_dir / "fundos_ativos.csv", encoding="utf-8-sig")
    df["vl_patrim_liq"] = pd.to_numeric(df["vl_patrim_liq"], errors="coerce").fillna(0)
    df["taxa_adm"] = pd.to_numeric(df["taxa_adm"], errors="coerce")
    df["rentab_fundo"] = pd.to_numeric(df["rentab_fundo"], errors="coerce")
    df["idade_anos"] = pd.to_numeric(df["idade_anos"], errors="coerce").fillna(0)
    df["dt_reg"] = pd.to_datetime(df["dt_reg"], errors="coerce")
    df["classe"] = df["classe"].fillna("Não classificada")
    df["gestor"] = df["gestor"].fillna("Não informado")
    df["denom_social"] = df["denom_social"].fillna("Sem nome")
    # PL em milhões pra legibilidade
    df["pl_milhoes"] = df["vl_patrim_liq"] / 1e6
    return df

df = carregar_dados()
total_ativos = len(df)
pl_total_str = f"{df['vl_patrim_liq'].sum()/1e9:,.2f}"
idademed = df["idade_anos"].mean()
cdi_ref = 14.15  # CDI anual de referência

# ═══════════════════════════════════════════════════
# SIDEBAR — FILTROS
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.title("📊 Dashboard")
    st.caption("Dados reais · CVM · maio/2026")
    st.divider()
    st.subheader("Filtros")
    classes_disponiveis = sorted(df["classe"].dropna().unique())
    classe_sel = st.multiselect("Classe do fundo", classes_disponiveis, default=classes_disponiveis)
    pl_min, pl_max = float(df["pl_milhoes"].min()), float(df["pl_milhoes"].max())
    pl_range = st.slider("Patrimônio Líquido (R$ milhões)", pl_min, pl_max, (pl_min, pl_max))
    gestores_disponiveis = sorted(df["gestor"].dropna().unique())
    gestor_sel = st.multiselect("Gestor", gestores_disponiveis, default=gestores_disponiveis)
    st.divider()
    st.caption("Paleta Itaú · Alto contraste · Alt-text em gráficos")

# Aplicar filtros
mask = (
    df["classe"].isin(classe_sel)
    & (df["pl_milhoes"] >= pl_range[0])
    & (df["pl_milhoes"] <= pl_range[1])
    & df["gestor"].isin(gestor_sel)
)
df_filtrado = df[mask].copy()

# ═══════════════════════════════════════════════════
# HEADER + KPIs
# ═══════════════════════════════════════════════════
st.title("Dashboard de Fundos Brasileiros")
st.caption("Dados públicos · CVM · CDI BCB")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Fundos", f"{len(df_filtrado)}")
with col2:
    pl_total = df_filtrado["vl_patrim_liq"].sum()
    st.metric("PL Total", f"R$ {pl_total/1e9:,.1f} B", help="Patrimônio líquido somado dos fundos filtrados")
with col3:
    st.metric("CDI (ref.)", f"{cdi_ref}% a.a.", help="Taxa CDI anualizada usada como benchmark")
with col4:
    st.metric("Idade Média", f"{df_filtrado['idade_anos'].mean():.1f} anos")

st.divider()

# ═══════════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ═══════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "🏢 Gestores", "📋 Dados Brutos"])

with tab1:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Fundos por Classe")
        if len(df_filtrado) > 0:
            dist = df_filtrado["classe"].value_counts().reset_index()
            dist.columns = ["Classe", "Qtd"]
            fig = px.bar(
                dist.sort_values("Qtd"),
                x="Qtd", y="Classe", orientation="h",
                text_auto=True,
                color="Qtd",
                color_continuous_scale=acessivel,
                title="Quantidade de Fundos por Classe",
            )
            fig.update_traces(textfont_size=14, textposition="outside", marker_line_width=0)
            fig.update_layout(
                template="plotly_dark",
                font=dict(size=14),
                title=dict(x=0.5, font=dict(size=18)),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                paper_bgcolor=BACKGROUND,
                plot_bgcolor=BACKGROUND,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Alt-text: barras horizontais com quantidade de fundos em cada classe de investimento")
        else:
            st.warning("Nenhum fundo encontrado com os filtros atuais.")

    with col_right:
        st.subheader("Patrimônio Líquido por Classe")
        if len(df_filtrado) > 0:
            pl_classe = df_filtrado.groupby("classe")["vl_patrim_liq"].sum().reset_index()
            pl_classe["PL_Bilhoes"] = pl_classe["vl_patrim_liq"] / 1e9
            fig = px.treemap(
                pl_classe,
                path=["classe"],
                values="PL_Bilhoes",
                color="PL_Bilhoes",
                color_continuous_scale=acessivel,
                title="PL por Classe (R$ Bilhões)",
            )
            fig.update_traces(texttemplate="%{label}<br>R$ %{value:.1f}B", textfont_size=14)
            fig.update_layout(
                template="plotly_dark",
                title=dict(x=0.5, font=dict(size=18)),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                paper_bgcolor=BACKGROUND,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Alt-text: treemap mostrando a concentração de patrimônio líquido por classe de fundo")
        else:
            st.warning("Nenhum fundo encontrado com os filtros atuais.")

    st.divider()
    st.subheader("Patrimônio vs Idade do Fundo")
    if len(df_filtrado) >= 2:
        fig = px.scatter(
            df_filtrado,
            x="idade_anos",
            y="pl_milhoes",
            color="classe",
            size="pl_milhoes",
            size_max=55,
            hover_name="denom_social",
            hover_data={"gestor": True, "classe": False, "pl_milhoes": ":.1f"},
            title="Patrimônio Líquido vs Idade do Fundo",
            color_discrete_sequence=PALETTE,
            log_y=True,
        )
        fig.update_layout(
            template="plotly_dark",
            font=dict(size=14),
            title=dict(x=0.5, font=dict(size=18)),
            xaxis_title="Idade (anos)",
            yaxis_title="PL (R$ milhões) — escala log",
            margin=dict(l=20, r=20, t=50, b=20),
            height=450,
            paper_bgcolor=BACKGROUND,
            plot_bgcolor=BACKGROUND,
            legend=dict(orientation="h", y=1.15),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Alt-text: dispersão do patrimônio líquido contra idade, colorido por classe. Escala logarítmica no eixo Y para lidar com a concentração do FI-FGTS")
    else:
        st.warning("Dados insuficientes para o gráfico de dispersão.")

# ═══════════════════════════════════════════════════
# ABA 2 — GESTORES
# ═══════════════════════════════════════════════════
with tab2:
    st.subheader("Concentração por Gestor")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        if len(df_filtrado) > 0:
            top = df_filtrado.groupby("gestor")["vl_patrim_liq"].sum().sort_values(ascending=False).head(10).reset_index()
            top["PL_Bilhoes"] = top["vl_patrim_liq"] / 1e9
            fig = px.bar(
                top.sort_values("PL_Bilhoes"),
                x="PL_Bilhoes", y="gestor", orientation="h",
                text_auto=".2f",
                color="PL_Bilhoes",
                color_continuous_scale=acessivel,
                title="Top 10 Gestores por PL",
            )
            fig.update_traces(textfont_size=13, textposition="outside", texttemplate="R$ %{x:.2f}B")
            fig.update_layout(
                template="plotly_dark",
                font=dict(size=14),
                title=dict(x=0.5, font=dict(size=18)),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                paper_bgcolor=BACKGROUND,
                plot_bgcolor=BACKGROUND,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Alt-text: barras horizontais com patrimônio líquido total por gestor")
        else:
            st.warning("Nenhum gestor encontrado com os filtros atuais.")

    with col_b:
        st.subheader("Market Share")
        if len(df_filtrado) > 0:
            total_pl = df_filtrado["vl_patrim_liq"].sum()
            share = df_filtrado.groupby("gestor")["vl_patrim_liq"].sum().sort_values(ascending=True)
            share_pct = (share / total_pl * 100).reset_index()
            share_pct.columns = ["Gestor", "Share_%"]
            # Agrupa gestores < 2% como "Demais"
            share_pct["label"] = share_pct.apply(
                lambda r: r["Gestor"] if r["Share_%"] >= 2 else "Demais", axis=1
            )
            share_agg = share_pct.groupby("label")["Share_%"].sum().sort_values().reset_index()

            fig = px.bar(
                share_agg,
                x="Share_%", y="label", orientation="h",
                text_auto=".1f",
                color="Share_%",
                color_continuous_scale=acessivel,
                title="Market Share por Gestor",
            )
            fig.update_traces(
                textfont_size=13, textposition="outside",
                texttemplate="%{x:.1f}%", marker_line_width=0,
            )
            fig.update_layout(
                template="plotly_dark",
                font=dict(size=14),
                title=dict(x=0.5, font=dict(size=18)),
                xaxis_title="% do PL Total",
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                paper_bgcolor=BACKGROUND,
                plot_bgcolor=BACKGROUND,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Alt-text: barras horizontais com percentual do patrimônio líquido total por gestor")
        else:
            st.warning("Dados insuficientes para market share.")

    # Métrica HHI
    if len(df_filtrado) >= 2:
        ms = df_filtrado["vl_patrim_liq"] / df_filtrado["vl_patrim_liq"].sum()
        hhi = (ms ** 2).sum() * 10000
        st.divider()
        hhi_col1, hhi_col2, hhi_col3 = st.columns([1, 2, 1])
        with hhi_col2:
            st.metric(
                "Índice Herfindahl-Hirschman (HHI)",
                f"{hhi:,.0f}",
                help="Mede concentração de mercado. <1500 = competitivo, 1500-2500 = moderado, >2500 = concentrado",
            )
            if hhi > 2500:
                st.warning(f"Mercado altamente concentrado. O maior gestor detém {df_filtrado.groupby('gestor')['vl_patrim_liq'].sum().max() / df_filtrado['vl_patrim_liq'].sum() * 100:.1f}% do PL.")
            elif hhi > 1500:
                st.info("Concentração moderada.")
            else:
                st.success("Mercado competitivo (baixa concentração).")

# ═══════════════════════════════════════════════════
# ABA 3 — DADOS BRUTOS
# ═══════════════════════════════════════════════════
with tab3:
    st.subheader("Dados Completos")
    cols_exibir = ["denom_social", "classe", "gestor", "pl_milhoes", "taxa_adm", "rentab_fundo", "idade_anos", "dt_reg"]
    cols_validas = [c for c in cols_exibir if c in df_filtrado.columns]
    df_display = df_filtrado[cols_validas].copy()
    df_display.columns = [
        "Nome do Fundo", "Classe", "Gestor",
        "PL (R$ milhões)", "Taxa ADM (%)", "Rentab. 12M (%)",
        "Idade (anos)", "Data Registro"
    ][:len(cols_validas)]
    df_display = df_display.sort_values("PL (R$ milhões)", ascending=False)
    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            "PL (R$ milhões)": st.column_config.NumberColumn(format="R$ %.1f M"),
            "Taxa ADM (%)": st.column_config.NumberColumn(format="%.2f%%"),
            "Rentab. 12M (%)": st.column_config.NumberColumn(format="%.2f%%"),
            "Idade (anos)": st.column_config.NumberColumn(format="%.1f"),
        },
        hide_index=True,
    )
    st.caption(f"{len(df_filtrado)} fundos exibidos de {total_ativos} totais")

# ═══════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════
st.divider()
st.caption(f"Dados: CVM (cad_fi.csv) + BCB (série 4390 CDI) · Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} · Rodrigo Cruz dos Santos")
