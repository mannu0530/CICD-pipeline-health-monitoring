# Deployment Guide

This guide explains how to deploy the CI/CD Pipeline Health Monitoring dashboard on AWS using Terraform.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform installed (version 1.0+)
- Git repository pushed to GitHub (update the GitHub URL in `infra/ec2.tf` if necessary)

## Steps

1. **Clone the repository and navigate to infra folder:**
   ```bash
   git clone <your-repo-url>
   cd CICD-pipeline-health-monitoring/infra
   ```

2. **Initialize Terraform:**
   ```bash
   terraform init
   ```

3. **Review the plan:**
   ```bash
   terraform plan
   ```

4. **Apply the infrastructure:**
   ```bash
   terraform apply
   ```
   Type `yes` when prompted.

5. **Get the public IP:**
   After deployment, note the `instance_public_ip` output from Terraform.

6. **Access the application:**
   Open a web browser and navigate to `http://<instance_public_ip>`

## Configuration

- **Region:** Default is `us-east-1`. Change in `provider.tf` if needed.
- **Instance Type:** `t2.micro` (free tier eligible).
- **GitHub URL:** Update in `ec2.tf` user_data script.

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

## Troubleshooting

- Ensure AWS credentials are configured.
- Check security group rules if unable to access the app.
- Verify the GitHub repository is public or accessible from the EC2 instance.