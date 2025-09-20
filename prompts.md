# AI Prompts Used for IaC and Deployment

This document records the AI prompts used to generate Terraform code, deployment scripts, and documentation for deploying the CI/CD Pipeline Health Monitoring app on AWS.

## Prompt 1: Generate Terraform Provider Configuration
**Prompt:** "Generate Terraform configuration for AWS provider with region variable for deploying infrastructure on AWS."

**Response:** Used to create `infra/provider.tf`.

## Prompt 2: Create VPC and Networking Resources
**Prompt:** "Write Terraform code to create a VPC with public subnet, internet gateway, and route table for AWS deployment."

**Response:** Used to create `infra/vpc.tf`.

## Prompt 3: Security Group for Web Application
**Prompt:** "Create AWS security group Terraform resource allowing SSH, HTTP, and HTTPS traffic for a web application."

**Response:** Used to create `infra/security_group.tf`.

## Prompt 4: EC2 Instance with Docker and App Deployment
**Prompt:** "Generate Terraform EC2 instance resource with user data script to install Docker, clone GitHub repo, and run docker-compose for a containerized app."

**Response:** Used to create `infra/ec2.tf`.

## Prompt 5: Deployment Guide
**Prompt:** "Write a deployment guide explaining how to use Terraform to provision AWS infrastructure and deploy a containerized application."

**Response:** Used to create `deployment.md`.

## AI Workflow Summary
- Used AI to generate modular Terraform files for each infrastructure component.
- Leveraged AI for writing user data scripts to automate Docker installation and app deployment.
- Employed AI to create comprehensive documentation and deployment instructions.
- Ensured all code follows Terraform best practices and AWS security guidelines.