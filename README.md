# Muro

## Rodando local

#### 1. Instale as dependências:

```console
pip install -r requirements.txt
```

#### 2. Baixe um json com dados de exemplo

```console
curl "http://muro.baixocentro.org/baixocentro.json" > static/baixocentro.json
```

#### 3. Rode o servidor

```console
python app.py
```

## Deploy

```console
git remote add heroku git@heroku.com:spvaiparar.git
git push heroku master
```
