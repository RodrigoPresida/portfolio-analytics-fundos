# Analytics de Fundos de Investimento BR 📊📈

> **Pipeline completo de engenharia e visualização de dados para análise de competitividade e concentração do mercado brasileiro de fundos.**

Este projeto demonstra a construção de um ecossistema analítico que consome dados reais da **CVM (Comissão de Valores Mobiliários)** para mapear o panorama atual de fundos de investimento no Brasil. O foco está em transformar dados brutos em inteligência estratégica, utilizando métricas como o **Índice HHI** para avaliar a concentração de mercado.

[**🔗 Acesse o Dashboard no Hugging Face Spaces**](https://huggingface.co/spaces/RodrigoPresida/portfolio-fundos)

---

## 🛠️ Tecnologias e Ferramentas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=Plotly&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow?style=for-the-badge)

---

## 🚀 Desafios e Soluções

### 1. Engenharia de Dados
O processo começa com a extração de dados públicos (CSV) da CVM. O principal desafio foi o tratamento de volumes financeiros (Patrimônio Líquido) e a limpeza de metadados inconsistentes para garantir que a análise de idade e classe dos fundos fosse precisa.

### 2. Análise Estratégica (Market Share)
Além de visualizar o saldo total, o projeto implementa o cálculo do **Herfindahl-Hirschman Index (HHI)**, uma métrica de economia industrial usada para determinar quão competitivo ou concentrado é um determinado segmento (ex: Renda Fixa vs Multimercado).

### 3. UI/UX & Storytelling
O dashboard foi desenvolvido em Streamlit com injeção de **CSS customizado** para sair do visual padrão da biblioteca e entregar uma experiência profissional, com hierarquia visual clara e cards de KPI de alto impacto.

---

## 📂 Estrutura do Repositório

- `dashboard.py`: O coração da aplicação, contendo a lógica de visualização e estilos customizados.
- `analise_real.py`: Script de processamento e saneamento dos dados brutos.
- `data/`: Amostra dos dados processados (ativos).
- `notebook.ipynb`: Exploração inicial e prototipagem das métricas de concentração.

---

## ⚙️ Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/RodrigoPresida/portfolio-analytics-fundos.git
   ```
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Rode o Dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

---

## 👤 Autor

**Rodrigo Presida** — *AI Architect & Data Scientist*
- [LinkedIn](https://www.linkedin.com/in/rodrigopresida)
- [GitHub](https://github.com/RodrigoPresida)

---
*Este projeto faz parte de um portfólio focado em demonstrar a união entre Engenharia de Dados, Finanças e UX.*
