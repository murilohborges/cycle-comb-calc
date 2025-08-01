# 🔬 Cycle Comb Calc - Microsserviço

Microsserviço desenvolvido com **Python** e **FastAPI** para realizar cálculos termodinâmicos relacionados ao ciclo combinado Brayton-Rankine à gás (como calor específico, entalpia, entropia, poder calorífico inferior, eficiências e potências geradas), utilizando fórmulas da literatura técnica.

---

## 📁 Estrutura do Projeto

```bash
cycle-comb-calc/
│
├── .devcontainer                   # Configurações do container para desenvolvimento
├── app/
│   ├── __init__.py                 # Define o pacote 'app'
│   ├── main.py                     # Ponto de entrada do microsserviço (FastAPI)
│   ├── routes/                     # Rotas da API
│   │   ├── __init__.py
│   │   ├── simulation.py           # Rota para o endpoint "/simulation"
│   │   └── substances.py           # Rota para o endpoint "/substances"
│   └── models/
│       ├── __init__.py
│       ├── input.py                # Schema Pydantic para validação de dados de entrada do endpoint para "/simulation"
│       ├── output.py               # Schema Pydantic para validação de dados de saída do endpoint para "/simulation"
│       └── substance.py            # Schema Pydantic para validação de dados de saída do endpoint para "/substances"
│
├── database/                       # Pasta com arquivos referentes ao banco de dados
│       ├── __init__.py
│       ├── create.py               # Script para executar a criação da engine do banco de dados
│       ├── default_substances.json # Arquivo json com os dados das substância padrão"
│       ├── engine.json             # Script para criação da engine do banco de dados"
│       ├── models.json             # Script com o modelos das tabelas e suas colunas do banco de dados"
│       └── seed.py                 # Script para popular do banco de dados com os dados das substâncias padrão"
│
├── requirements.txt                # Lista de dependências do projeto
├── .gitignore                      # Arquivos/pastas ignorados pelo Git
└── README.md                       # Documentação do projeto
```


## 🚀 Como executar

1. Clone o repositório:
```bash
git clone git@github.com:seu-usuario/cycle-comb-calc.git

cd cycle-comb-calc
```
<br>

2. Clone o repositório:
```bash
python -m venv venv
```
<br>

3. Ative o ambiente virtual:
- Linux/macOS:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```
<br>

4. Ative o ambiente virtual:
```bash
pip install -r requirements.txt
```
<br>

5. Execute o comando para criar e popular o banco de dados com dados padrão:
```bash
python -m app.database.seed
```
<br>

6. Execute o servidor:
```bash
uvicorn app.main:app --reload
```
Acesse em: http://localhost:8000/docs


## ✅ Testes
Para executar os testes:
```
pytest
```

## 📚 Referência Acadêmica

Este projeto é baseado no Trabalho de Conclusão de Curso (TCC) apresentado no curso de Engenharia Química:

**Título**: *Desenvolvimento de um aplicativo para cálculos de ciclos combinados*
<br>
[Acesse aqui o TCC](https://admin-pergamum.ifsuldeminas.edu.br/pergamumweb/vinculos/000064/00006417.pdf)


