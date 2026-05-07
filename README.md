# End-to-End DevOps Pipeline: Microservice with CI/CD & IaC

This repository demonstrates a complete, automated DevOps lifecycle for a modern microservice. It showcases the integration of containerization, continuous integration/continuous deployment (CI/CD), and Infrastructure as Code (IaC) to deliver a reliable and scalable application.

## 🚀 Architecture & Workflow

1. **Application:** A lightweight REST API built with Python and FastAPI.
2. **Containerization:** The application is packaged using a multi-stage `Dockerfile` for consistency across environments.
3. **CI/CD Pipeline:** GitHub Actions automatically triggers on every push to the `main` branch. It runs automated tests (pytest), builds the Docker image, and pushes it to Docker Hub.
4. **Infrastructure as Code (IaC):** Terraform scripts are used to provision an AWS EC2 instance, configure security groups, and automatically deploy the containerized application upon server initialization.

## 🛠️ Technologies Used

* **Code & Framework:** Python 3.11, FastAPI
* **Testing:** Pytest
* **Containerization:** Docker
* **CI/CD:** GitHub Actions
* **Infrastructure as Code:** Terraform
* **Cloud Provider:** AWS (Amazon Web Services)
* **Container Registry:** Docker Hub

## 📂 Project Structure

```text
.
├── .github/workflows/
│   └── ci-cd.yml          # GitHub Actions pipeline configuration
├── main.py                # FastAPI application source code
├── test_main.py           # Automated unit tests
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── main.tf                # Terraform infrastructure script
└── README.md              # Project documentation
