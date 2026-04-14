# GeoJSON Highway Generator

Interface web para geocodificar rodovias brasileiras e exportar os resultados em formato GeoJSON, utilizando a API do Google Maps.

## Funcionalidades

- Geocodifica as 5 rodovias de referência via Google Geocoding API
- Exporta um arquivo `.geojson` com as coordenadas e metadados
- Download direto pelo navegador
- Visualização do JSON gerado na própria interface

## Pré-requisitos

- Python 3.10+
- Chave de API do Google Cloud com a **Geocoding API** habilitada

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/geojson-highway-generator.git
cd geojson-highway-generator

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com sua chave de API:

```
GOOGLE_API_KEY=AIzaSua_Chave_Aqui
```

> O `.env` está no `.gitignore` e nunca será enviado ao repositório.

Alternativamente, você pode inserir a chave diretamente no campo da interface ao rodar o app.

## Uso

```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador, informe a API Key (se não estiver no `.env`) e clique em **Geocodificar e Gerar GeoJSON**.

O arquivo gerado é salvo em `output/saida_artesp.geojson` e também disponibilizado para download direto pela interface.

## Estrutura

```
.
├── app.py            # Aplicação Streamlit
├── requirements.txt  # Dependências
├── .env              # Chave de API (não versionar)
└── output/           # GeoJSONs gerados (não versionado)
```

## Dependências

| Pacote | Uso |
|--------|-----|
| `streamlit` | Interface web |
| `requests` | Chamadas à API do Google Maps |
