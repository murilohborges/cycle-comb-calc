# 🔬 Cycle Combustion Calc - Microsserviço

Microsserviço desenvolvido com **Python** e **FastAPI** para realizar cálculos termodinâmicos relacionados ao ciclo combinado Brayton-Rankine à gás (como calor específico, entalpia, entropia, poder calorífico inferior, eficiências e potências geradas), utilizando fórmulas da literatura técnica.

---

## 📁 Estrutura do Projeto

```bash
cycle-comb-calc/
│
├── app/
│   ├── __init__.py             # Define o pacote 'app'
│   ├── main.py                 # Ponto de entrada do microsserviço (FastAPI)
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # Rotas da API
│   ├── services/
│   │   └── calculations.py     # Lógica dos cálculos termodinâmicos
│   └── models/
│       └── schemas.py          # Schemas Pydantic para validação de dados
│
├── tests/                      # Testes com pytest
│   └── test_calculations.py
│
├── requirements.txt            # Lista de dependências do projeto
├── .gitignore                  # Arquivos/pastas ignorados pelo Git
└── README.md                   # Documentação do projeto
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

5. Execute o servidor:
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


