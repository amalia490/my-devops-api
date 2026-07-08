# End-to-End DevOps Pipeline: GraphQL Microservice cu CI/CD & IaC

>  **Proiect în derulare (Work in Progress):** Acest proiect se află în dezvoltare activă. În prezent mă concentrez pe implementarea și securizarea infrastructurii serverului (AWS/Terraform) conform celor mai bune practici de securitate, precum și pe dezvoltarea aplicației de **Frontend** care va consuma acest API.

Acest repository demonstrează un ciclu complet și automatizat de DevOps pentru o aplicație modernă. Proiectul ilustrează integrarea containerizării, a fluxurilor de CI/CD și a conceptului de Infrastructure as Code (IaC) pentru a livra o aplicație scalabilă, testată și robustă.

##  Arhitectură & Flux de Lucru

* **Aplicație Backend:** Un API robust construit cu Python, **FastAPI** și **GraphQL** (via Strawberry). Datele sunt gestionate prin **SQLModel** și stocate într-o bază de date PostgreSQL, versiunile schemei fiind controlate prin migrații automate cu **Alembic**.
* **Arhitectură Monorepo:** Codul este împărțit logic în foldere independente pentru `backend` și `frontend` (în curs de dezvoltare).
* **Containerizare:** Componentele sunt împachetate folosind Docker (cu fișiere Dockerfile multi-stage) pentru a asigura rularea identică în orice mediu (Local, Testare, Producție).
* **CI/CD Pipeline:** GitHub Actions declanșează automat un pipeline la fiecare push pe ramura `main`. Acest robot creează baze de date de test în memorie (SQLite), rulează testele automate (`pytest`), construiește imaginea de Docker și o trimite către Docker Hub.
* **Infrastructure as Code (IaC):** Scripturile Terraform sunt utilizate pentru a proviziona infrastructura în AWS (EC2), a configura Security Groups și a asigura un mediu sigur și reproductibil pentru deploy.

##  Tehnologii Utilizate

**Backend & Baze de Date:**
* **Limbaj & Framework:** Python 3.11, FastAPI
* **API:** GraphQL (Strawberry)
* **Bază de date & ORM:** PostgreSQL, SQLModel
* **Migrații:** Alembic
* **Testare:** Pytest (cu baze de date in-memory izolate)

**DevOps & Infrastructură:**
* **Containerizare:** Docker & Docker Compose
* **CI/CD:** GitHub Actions
* **Infrastructure as Code:** Terraform
* **Cloud Provider:** AWS (Amazon Web Services)
* **Container Registry:** Docker Hub

##  Structura Proiectului

```text
.
├── .github/workflows/
│   └── ci-cd.yml              # Configurația pipeline-ului GitHub Actions
├── backend/
│   ├── alembic/               # Scripturile de migrare a bazei de date
│   ├── tests/                 # Testele unitare și de integrare (Pytest)
│   ├── main.py                # Punctul de intrare pentru aplicația FastAPI
│   ├── schema.py              # Schema și resolverele GraphQL (Strawberry)
│   ├── models.py              # Modelele bazei de date (SQLModel)
│   ├── db.py                  # Conexiunea la PostgreSQL
│   ├── alembic.ini            # Configurația pentru migrații
│   ├── requirements.txt       # Dependențele Python
│   └── Dockerfile             # Fișierul de build Docker pentru backend
├── frontend/                  #  WIP: Aplicația de frontend (Node.js/React etc.)
├── infra/                     
│   └── main.tf                # Scriptul de infrastructură Terraform (AWS)
├── docker-compose.yml         # Orchestarea locală (Backend + Baza de date)
├── .gitignore                 # Excluderi pentru secrete și cache
└── README.md                  # Documentația proiectului
