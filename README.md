# End-to-End DevOps Pipeline: GraphQL Microservice with CI/CD & IaC

> ⚠️ **Work in Progress (WIP):** This project is under active development. My current focus areas include:
> * **Performance Optimization:** Implementing a **DataLoader** layer to batch and cache GraphQL queries, effectively eliminating the N+1 problem.
> * **Infrastructure & Security:** Finalizing the AWS server provisioning (Terraform) following security best practices.
> * **Frontend:** Developing the client-side application that will consume this API.

##  Architecture & Workflow

* **Backend Application:** A robust API built with Python, **FastAPI**, and **GraphQL** (via Strawberry). Data is managed through **SQLModel** and stored in a PostgreSQL database, with schema versions controlled via automated migrations using **Alembic**.
* **Monorepo Architecture:** The codebase is logically separated into independent directories for the `backend` and `frontend` (in development).
* **Containerization:** Components are packaged using Docker (featuring multi-stage Dockerfiles) to ensure consistent execution across any environment (Local, Testing, Production).
* **CI/CD Pipeline:** GitHub Actions automatically triggers a pipeline on every push to the `main` branch. This workflow provisions isolated in-memory test databases (SQLite), runs automated tests (`pytest`), builds the Docker image, and pushes it to Docker Hub.
* **Infrastructure as Code (IaC):** Terraform scripts are used to provision infrastructure in AWS (EC2), configure Security Groups, and ensure a secure and reproducible deployment environment.

##  Technologies Used

**Backend & Databases:**
* **Language & Framework:** Python 3.11, FastAPI
* **API:** GraphQL (Strawberry)
* **Database & ORM:** PostgreSQL, SQLModel
* **Migrations:** Alembic
* **Testing:** Pytest (with isolated in-memory databases)

**DevOps & Infrastructure:**
* **Containerization:** Docker & Docker Compose
* **CI/CD:** GitHub Actions
* **Infrastructure as Code:** Terraform
* **Cloud Provider:** AWS (Amazon Web Services)
* **Container Registry:** Docker Hub

## Project Structure

```text
.
├── .github/workflows/
│   └── ci-cd.yml              # GitHub Actions pipeline configuration
├── backend/
│   ├── alembic/               # Database migration scripts
│   ├── tests/                 # Unit and integration tests (Pytest)
│   ├── main.py                # Entry point for the FastAPI application
│   ├── schema.py              # GraphQL schema and resolvers (Strawberry)
│   ├── models.py              # Database models (SQLModel)
│   ├── db.py                  # PostgreSQL connection setup
│   ├── alembic.ini            # Alembic configuration file
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Docker build file for the backend
├── frontend/                  # WIP: Frontend application (Node.js/React etc.)
├── main.tf                    # Terraform infrastructure script (AWS)
├── docker-compose.yml         # Local orchestration (Backend + Database)
├── .gitignore                 # Exclusions for secrets, cache, and environments
└── README.md                  # Project documentation
