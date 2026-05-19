# Rascunho — Postagem LinkedIn (ate 1200 caracteres)

---

Dados publicos + Python + AWS: montei um estudo sobre o mercado de fundos brasileiro que vai da coleta ate a nuvem.

O notebook coleta dados reais da CVM, BCB e BrasilAPI, faz ETL completo, analise exploratoria e visualizacoes interativas com Plotly — tudo rodando local, sem API key, sem cloud. Mas a parte que eu mais gostei de fazer foi a discussao sobre como esse pipeline escala: S3, Glue, Athena, QuickSight. O tipo de arquitetura que transforma CSV em Data Lake com governanca.

O que tem la:
- Coleta modular com fallback (API caiu? nao quebra)
- EDA com metricas de negocio e benchmark CDI
- Graficos interativos com acessibilidade (alto contraste, alt-text)
- Arquitetura AWS conceitual com justificativa de custo
- Acessibilidade como principio, nao como checklist

Ta aberto no GitHub:

github.com/RodrigoPresida/portfolio-analytics-fundos

#Python #AWS #DataAnalytics #FundosDeInvestimento #OpenSource #DadosPublicos #Acessibilidade #DataScience
