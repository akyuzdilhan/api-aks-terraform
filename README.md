# Automate All The Things: REST API Deployment with AKS

## Overview
This project demonstrates the deployment of a REST API using Azure Kubernetes Service (AKS) and Terraform. The API provides:
- Current time in different formats and zones.
- A static message: "Automate All The Things."

## Features
- **Python (FastAPI)**: Lightweight and fast API framework.
- **Docker**: Application containerization for portability and consistency.
- **Terraform**: Infrastructure as Code for Azure resources and Kubernetes configurations.
- **Azure Services**:
  - Azure Kubernetes Service (AKS) for container orchestration.
  - Azure Container Registry (ACR) for Docker image storage.

## Project Structure
```plaintext
AUTOMATEALLTHETHINGS/
├── api/
│   ├── main.py           # REST API source code
│   └── requirements.txt  # Python dependencies
├── terraform/
│   ├── acr.tf            # ACR setup
│   ├── aks.tf            # AKS setup
│   ├── k8s.tf            # Kubernetes configuration
│   ├── main.tf           # Main Terraform configuration
│   ├── variables.tf      # Variables for Terraform
│   ├── outputs.tf        # Output values
│   └── versions.tf       # Provider version requirements
├── Dockerfile            # Docker image configuration
├── .gitignore            # Files and directories to exclude from Git
└── README.md             # Project documentation
