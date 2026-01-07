# ⚡ Combined Cycle Power Plant Calculator - Microservice

This project is a backend microservice designed to perform thermodynamic calculations
commonly used in Combined Cycle Power Plants (CCPP), which integrate gas turbine
(Brayton cycle) and steam turbine (Rankine cycle) systems for thermal power generation.

The service exposes calculation logic through a RESTful API built with **Python** and **FastAPI**,
allowing external applications to request cycle parameters, efficiencies, and
thermodynamic properties in a structured and scalable way.

While the thermodynamic calculations are based on an academic project, the main goal
of this repository is to apply software engineering practices by exposing the logic
as a RESTful microservice, designed to be consumed by a web application or other
distributed systems.

**Live API:** [cycle-comb-calc.onrender.com/docs](https://cycle-comb-calc.onrender.com/docs)

---

## 📁 Project Structure

```bash
cycle-comb-calc/
│
├── .devcontainer/                  # Development container configuration (for VS Code Remote Containers)
├── .vscode                         # Editor-specific settings for VS Code
├── app/
│   ├── controllers/                # Controllers responsible for handling endpoint actions
│   ├── database/                   # Database-related files (connection, initialization, seeding)
│   ├── models/                     # Pydantic schemas used for data validation and serialization
│   ├── repositories/               # Data access layer that interacts with the database
│   ├── routes/                     # API routes mapping endpoints to controllers
│   ├── services/                   # Business logic and calculation classes of the application
│   ├── utils/                      # Utility modules and helper functions
│   └── main.py                     # Microservice entry point (FastAPI)
│
├── tests/                          # Unit and integration test files
├── .editorconfig                   # Editor configuration to maintain consistent code style
├── .gitignore                      # Files/folders ignored by Git
├── LICENSE                         # Project license
├── pytest.ini                      # Pytest configuration file
├── docker-compose.yml              # Docker Compose configuration for local deployment
├── Dockerfile                      # Docker build instructions
├── entrypoint.sh                   # Container startup script
├── README.md                       # Project documentation
└── requirements.txt                # Project dependency list
```


## 🚀 Running Locally (Manual Setup)

1. Clone the repository:
```bash
git clone git@github.com:murilohborges/cycle-comb-calc.git

cd cycle-comb-calc
```
<br>

2. Create a virtual environment:
```bash
python -m venv venv
```
<br>

3. Activate the virtual environment:
- Linux/macOS:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```
<br>

4. Install the required packages:
```bash
pip install -r requirements.txt
```
<br>

5. Create and populate the database with default data:
```bash
python -m app.database.seed
```
<br>

6. Run the development server:
```bash
uvicorn app.main:app --reload
```


## 🐳 Running with Docker (Recommended)

1. Build and start the container:
```bash
docker compose up --build
```
<br>

2. Access the API:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
<br>
<br>

3. Stop and remove the container:
```bash
docker compose down
```
💾 The SQLite database is persisted via a Docker volume defined in docker-compose.yml.This ensures data is not lost when the container is rebuilt.


## 🧭 API Documentation

Once the server is running, open your browser and go to:

➡️ **Swagger UI:** `http://<your-local-address>:<port>/docs`  
➡️ **ReDoc:** `http://<your-local-address>:<port>/redoc`

> 💡 *By default, FastAPI runs on* `http://127.0.0.1:8000` *or* `http://localhost:8000`


## ✅ Running Tests
To run all tests:
```
pytest
```

If you prefer to run tests inside the Docker container:
```
docker compose exec api pytest
```

## 🌐 CORS Configuration

The service uses FastAPI’s CORS middleware to allow requests from specific frontends.

Allowed origins:

- http://localhost:5173 – Local frontend development

- https://cyclecombcalc.netlify.app/ – Production frontend

Configuration is located in `app/main.py`

## 📚 Academic Reference

This project is based on the final paper presented for the Chemical Engineering degree:

**Title**: *Development of an application for combined cycle calculations*
<br>
[Access the full paper here](https://admin-pergamum.ifsuldeminas.edu.br/pergamumweb/vinculos/000064/00006417.pdf)

---