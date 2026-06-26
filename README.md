# 🌱 go-green.house

> Acompanhamento do crescimento da **Maria** e da **Sofia**, comparado aos padrões de crescimento infantil da OMS.

[![deploy-book](https://github.com/eu-cristofer/go-green.house/actions/workflows/deploy.yml/badge.svg)](https://github.com/eu-cristofer/go-green.house/actions/workflows/deploy.yml)
[![site](https://img.shields.io/badge/site-go--green.house-1abc9c)](https://go-green.house)
[![Jupyter Book](https://img.shields.io/badge/feito%20com-Jupyter%20Book-f37726)](https://jupyterbook.org)
[![License: CC BY 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY%204.0-lightgrey)](LICENSE)

Um pequeno **Jupyter Book** que registra as medidas antropométricas das nossas garotinhas — peso, estatura e perímetro cefálico — e as sobrepõe, ao longo do tempo, às curvas de referência (escore-z) da **Organização Mundial da Saúde**.

A ideia é simples: cada consulta vira um ponto no gráfico. Unindo os pontos, surge a curva de crescimento de cada criança — uma forma visual e tranquila de acompanhar se tudo segue dentro do esperado.

---

## 📈 O que tem aqui

- **Peso para a idade**, **estatura para a idade** e **perímetro cefálico para a idade**
- Pontos individuais da Maria e da Sofia sobre as curvas de referência da OMS (−3, −2, 0, +2, +3 desvios‑padrão)
- Gráficos **interativos** em Plotly
- Tabelas com o registro de cada medição

## 🛠️ Como é construído

| Camada | Ferramenta |
| --- | --- |
| Conteúdo | Notebooks Jupyter + Markdown |
| Processamento | `pandas`, `numpy`, `openpyxl` |
| Visualização | `plotly` |
| Publicação | [Jupyter Book](https://jupyterbook.org) |
| CI/CD | GitHub Actions → GitHub Pages (domínio `go-green.house`) |

A cada `push` na branch `main`, o GitHub Actions reconstrói o livro e publica em **[go-green.house](https://go-green.house)**.

## 🚀 Rodando localmente

```bash
# 1. instalar dependências
pip install -r requirements.txt
pip install jupyter-book

# 2. construir o livro
jupyter-book build .

# 3. abrir o resultado
open _build/html/index.html      # macOS
# xdg-open _build/html/index.html  # Linux
```

Para limpar uma build anterior: `jupyter-book clean .`

## 📁 Estrutura

```
go-green.house/
├── _config.yml              # configuração do Jupyter Book
├── _toc.yml                 # sumário (table of contents)
├── references.bib           # referências bibliográficas
├── requirements.txt         # dependências Python
├── img/
│   └── logo.png
├── content/
│   ├── main_script.ipynb    # notebook principal (os gráficos)
│   ├── data_processing.py   # carga dos dados + função de plotagem
│   ├── sources.md           # notas e fontes dos dados
│   ├── DB_Maria.json        # medições da Maria
│   ├── DB_Sofia.json        # medições da Sofia
│   └── ref/                 # tabelas de referência da OMS (.xlsx)
└── .github/workflows/
    └── deploy.yml           # build + deploy automático
```

## 🩺 Fonte dos dados

As curvas de referência vêm dos **WHO Child Growth Standards**:
<https://www.who.int/tools/child-growth-standards/standards/weight-for-age>

Observações sobre tratamento e lacunas dos dados estão em [`content/sources.md`](content/sources.md).

## ➕ Adicionando uma nova medição

As medições ficam em `content/DB_Maria.json` e `content/DB_Sofia.json`, indexadas por data. Para registrar uma consulta nova, acrescente uma entrada no formato:

```json
"2025-06-26": {
  "Peso": 14.2,
  "Estatura": 96.0,
  "Perímetro Cefálico": 48.5
}
```

No próximo `push`, o gráfico se atualiza sozinho.

## ✍️ Autor

**Cristofer Antoni Souza Costa**

## 📄 Licença

Conteúdo sob [Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE).
Os dados de crescimento são padrões públicos da Organização Mundial da Saúde.