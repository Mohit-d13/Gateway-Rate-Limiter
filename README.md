# GATEWAY RATE LIMITER

Gateway rate limiter is a rate limiter that works as an inline filter with a gateway api. Rate limiter is primarily used to limit the amount of traffic a user or client can make to a web appliation within a specific timeframe.

## Feature

- Rate Limiter - Protects Backend infrastructure from being overwhelmed, prevents service outages and ensures fair access and resource availability for all legitimate users.

- Algorithm - Token Bucket algorithm is used for rate limiting. It controls traffic by storing a fixed maximum number of tokens in a "bucket" and consuming them as requests arrive.

- Database - To check/update rate-limiter state in fractions of a millisecond and to avoid race conditions with multiple app server Redis in-memory database is utilise.

- Versioning & Changlog - Automated CHANGELOG generation, the creation of GitHub releases, and version bumps by parsing git history convential commit messages via Github Actions.

- Continuous Integration (CI) - Automated integration tests, security tests and publishing container image with mutli tag on to GHCR and DockerHub via Github Actions.

- Continuous Deployment (CD) - Automated Deployment by setting up OIDC with AWS and deploying Helm chart on to AWS EKS cluster via Github Actions.

## Tech Stack

- Language & Runtime: Python
- Framework: FastAPI
- Package Manager: UV
- Database: Redis
- Containerization: Docker
- Container Orchetration: Docker Compose, Kubernetes + Helm Chart
- CI/CD: Github Actions
- Cloud Techology: AWS, eksctl
