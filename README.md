# GATEWAY RATE LIMITER

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688)
![Redis](https://img.shields.io/badge/Redis-Database-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED)
[![Release](https://img.shields.io/github/v/release/mohitd-13/gateway-rate-limiter)](https://github.com/mohitd-13/gateway-rate-limiter/releases)
[![Integration tests](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/integration-test.yml/badge.svg)](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/integration-test.yml)
[![Security scan](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/security-test.yml/badge.svg)](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/security-test.yml)
[![Create release](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/release-please.yml/badge.svg)](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/release-please.yml)
[![Publish Image](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/publish-images.yml/badge.svg)](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/publish-images.yml)
[![Deploy Application](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/deploy-to-eks.yml/badge.svg)](https://github.com/mohitd-13/gateway-rate-limiter/actions/workflows/deploy-to-eks.yml)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5)
![Helm](https://img.shields.io/badge/Helm-Chart-0F1689)
![AWS EKS](https://img.shields.io/badge/AWS-EKS-FF9900)
![License](https://img.shields.io/badge/License-MIT-green)

Gateway Rate Limiter is a FastAPI-based rate limiting service designed to operate as an inline Gateway API filter. It implements the token bucket algorithm using Redis as an centralized, in-memory state manager across distributed systems. Github Actions provides the full (CI/CD) automation of application lifecycle from integration, testing, creating new releases and even publishing container images on to container registries, and deploying the app on to local machine with Docker compose as well on to cloud with Kubernetes + Helm.

## Table of Contents

- [Feature](#feature)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Prerequisties](#prerequisties)
  - [Installations](#installations)
- [Repository Structure](#repository-structure)
- [Architecture Overview](#architecture-overview)
- [Example API Endpoints](#example-api-endpoints)
- [Contribution](#contributing)
- [License](#license)

## Feature

- Rate Limiter - Protects Backend infrastructure from being overwhelmed, prevents service outages and ensures fair access and resource availability for all legitimate users.

- Algorithm - Token Bucket algorithm is used for rate limiting. It controls traffic by storing a fixed maximum number of tokens in a "bucket" and consuming them as requests arrive.

- Database - To check/update rate-limiter state in fractions of a millisecond and to avoid race conditions with multiple app server Redis in-memory database is utilise.

- Versioning & Changlog - Automated CHANGELOG generation, the creation of GitHub releases, and version bumps by parsing git history convential commit messages via Github Actions.

- Continuous Integration (CI) - Automated integration tests, security tests and publishing container image with mutli tag on to GHCR and DockerHub via Github Actions.

- Continuous Deployment (CD) - Automated Deployment by setting up OIDC with AWS and deploying Helm chart on to AWS EKS cluster via Github Actions.

## Tech Stack

- **Language & Runtime**: Python
- **Framework**: FastAPI
- **Package Manager**: UV
- **Database**: Redis
- **Containerization**: Docker
- **Container Orchetration**: Docker Compose, Kubernetes + Helm Chart
- **CI/CD**: Github Actions
- **Cloud Techology**: AWS, eksctl

## Quick Start

### Prerequisties

- Docker & Docker Compose
- Kubernetes cluster (kind, minikube, k3d etc)
- kubectl
- Helm
- AWS Account & CLI (only for cloud)

### Installations

1. Clone the repository.

    ```bash
    git clone https://github.com/mohitd-13/gateway-rate-limiter.git
    cd rate-limiter
    ```

2. Create password inside secrets folder

    ```bash
    mkdir -p secrets/redis-creds
    echo "my-password" > secrets/redis-creds/password
    ```

    [!NOTE]
    Do not change the name of the path/folder only replace my-password

3. Run the application

    - On to Local machine with Docker compose

        ```bash
        docker compose up --build --watch
        ```

    - On to Local machine with Helm

        a. Create secret resource from password file

        ```bash
        kubectl create secret generic redis-secret \
        --from-file secret/redis/password \
        --dry-run=client -o yaml > \
        deployment/rate-limiter-chart/templates/
        ```

        b. Install Chart

        ```bash
        helm upgrade -i gateway ./deployment/rate-limiter-chart \
        --namespace gateway \
        --create-namespace
        ```

## Repository Structure

```text
.
├── .github
│   └── workflows
│       ├── deploy-to-eks.yml           # Automate deployment to eks cluster
│       ├── integration-test.yml        # Automate integration test on push 
│       ├── publish-images.yml          # Automate releasing container image
│       ├── release-please.yml          # Automate release tag, notes etc
│       └── security-test.yml           # Automate security scan on pr
├── .pre-commit-config.yaml             # pre-commit lint + format check
├── CHANGELOG.md                        # Commit history logs
├── compose.yaml                        # Multi-container configuration file 
├── core
│   ├── client.py                       # Initialize redis client
│   ├── config.py                       # Read configuration values
│   ├── identity.py                     # Extract identity
│   ├── __init__.py
│   ├── main.py                         # Main fastapi object and routes 
│   ├── policy.py                       # create dynamic policies
│   ├── schemas.py                      # Data models for(identity, policies)
│   └── utils.py
├── deployment
│   ├── aws-eks                         # Aws eks cluster configuration
│   └── rate-limiter-chart              # Main deployment resource chart
├── dev.Dockerfile                      # Development style container image                     
├── prod.Dockerfile                     # Production style container image
├── pyproject.toml                      # Project configuration file
├── README.md                           # Project notes and installation document
├── secrets
│   └── redis-creds
|       └── password                    # Database password file
├── tests
│   ├── __init__.py
│   └── test_main.py                    # Unit tests by pytest
└── uv.lock                             # Project Dependencies
```

## Architecture Overview

### Backend

- Built with Python framework FastAPI.
- Handles rate limiting logic, extract identity and configure dynamic policies.

### Database

- For fast in-memory database redis is used.
- Atomic operation via Lua Script for faster response time, provides near-instantaneous read and write operations.

### CI/CD Architecture Overview

![CI/CD Architecture Overview](https://private-user-images.githubusercontent.com/141726272/620471584-a4ae5a61-3e82-47c2-94a5-f2de99438493.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODM3OTI1MjgsIm5iZiI6MTc4Mzc5MjIyOCwicGF0aCI6Ii8xNDE3MjYyNzIvNjIwNDcxNTg0LWE0YWU1YTYxLTNlODItNDdjMi05NGE1LWYyZGU5OTQzODQ5My5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNzExJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDcxMVQxNzUwMjhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yMDdkOGVjMDdmYTcyMGIxMmJkNjYzNTcwMTczZmJjZjhmNzlkMmEyZjZmYjgzMGIxMzY3ODZjYzc2YjZkMjFhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.u_95BZ5aRFsKXGC-TJXvUuyk_7OqMER1Zf82Tucxq-A)

## Example API Endpoints

### Admin Routes

| Endpoint                                | Method | Description      |
|-----------------------------------------|--------|------------------|
| /admin/policy/{dimension}/{identity_id} | PUT    | Setup new Policy |
| /admin/policy/{dimension}/{identity_id} | GET    | Read Policy      |

### Health Check Route

| Endpoint | Method | Description     |
|----------|--------|-----------------|
| /        | GET    | Welcome Message |
| /healthz | GET    | Health Status   |

## Contributing

We welcome contributions from developers who want to improve Gateway-Rate-Limiter
Follow these steps to contribute effectively:

1. **Fork the Repository**

    - Click the Fork button on Github to create your own copy of the project.

2. **Clone Your Fork**

    - Run

    ```bash
    git clone https://github.com/mohitd-13/gateway-rate-limiter.git
    ```

3. **Set Up Database password**

    - Follow the setup instructions in the README to setup your password make sure not to change any path/folder name, if you do change the path/folder name you have to make changes in compose.yaml and helm values.yaml also. You can set the password of your choice.

4. **Create a Feature Branch**

    - Keep your changes organized:

    ```bash
    git checkout -b feature/your-feature-name
    ```

5. **Use Clear Commit Messages**

    - Make sure to always follow the conventional commit style without it, automated release process will not happen:
        - feat: - new feature
        - fix: - bug fix
        - BREAKING CHANGE: - new changes that are not backward-compatible
        - docs: - documentation update
        - refractor: - code restructuring

    - Document Your Changes
        - Update README.md or CONTRIBUTING.md if needed

6. **Submit a Pull Request (PR)**

    - Push your branch and open a PR with:

        - A short, clear description of your changes.
        - Any related issue numbers (for example, "Closes #12").
        - Screenshots or example outputs (if applicable).

7. **Participate in Code Review**

    - Respond to feedback, make improvements, and help maintain project quality.

## License

This project is licensed under the MIT License-see the LICENSE file for details.
