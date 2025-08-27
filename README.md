# CI/CD Pipeline Health Dashboard

A comprehensive web application to monitor and visualize CI/CD pipeline executions from multiple tools including GitHub Actions, GitLab CI, and Jenkins.

## 🚀 Features

- **Real-time Monitoring**: Track pipeline executions, build statuses, and performance metrics
- **Multi-tool Support**: GitHub Actions, GitLab CI, Jenkins integration
- **Metrics Dashboard**: Success/failure rates, average build times, last build status
- **Alerting System**: Slack and email notifications for pipeline failures and successes
- **Log Visualization**: Display build logs and execution details
- **Modern UI**: Clean, responsive interface built with React

## 🏗️ Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (Python)      │◄──►│   (MongoDB)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │  Alert Service  │              │
         │              │  (Slack/Email)  │              │
         │              └─────────────────┘              │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GitHub Actions │    │   GitLab CI     │    │     Jenkins     │
│   Webhooks      │    │   Webhooks      │    │   Webhooks      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: React.js with Material-UI
- **Backend**: Python Flask with REST API
- **Database**: MongoDB
- **Containerization**: Docker & Docker Compose
- **Alerting**: Slack API & SMTP for email

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.8+ (for local development)
- MongoDB (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cicd
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MongoDB: localhost:27017

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Start MongoDB locally or use Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/cicd_dashboard

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL_ID=C1234567890

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your-webhook-secret

# GitLab Configuration
GITLAB_WEBHOOK_SECRET=your-webhook-secret

# Jenkins Configuration
JENKINS_URL=http://your-jenkins-url
JENKINS_USERNAME=your-username
JENKINS_API_TOKEN=your-api-token
```

## 📊 API Endpoints

### Pipeline Data
- `GET /api/pipelines` - List all pipelines
- `GET /api/pipelines/<id>` - Get pipeline details
- `GET /api/pipelines/<id>/logs` - Get pipeline logs
- `GET /api/metrics` - Get dashboard metrics

### Webhooks
- `POST /api/webhooks/github` - GitHub Actions webhook
- `POST /api/webhooks/gitlab` - GitLab CI webhook
- `POST /api/webhooks/jenkins` - Jenkins webhook

### Alerts
- `POST /api/alerts/test` - Test alert configuration

## 🐳 Docker

### Build Images
```bash
docker-compose build
```

### Run Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Monitoring & Alerts

### Metrics Collected
- Pipeline execution status (success/failure)
- Build duration
- Success/failure rates
- Last build timestamp
- Build queue length

### Alert Triggers
- Pipeline failure
- Pipeline success (configurable)
- Build timeout
- High failure rate threshold

### Alert Channels
- **Slack**: Real-time notifications with build details
- **Email**: Daily/weekly summaries and critical alerts

## 🔒 Security

- Webhook signature verification
- API rate limiting
- Environment variable encryption
- CORS configuration
- Input validation and sanitization

## 🚀 Deployment

### Production Deployment
1. Update environment variables for production
2. Configure production MongoDB instance
3. Set up reverse proxy (nginx)
4. Configure SSL certificates
5. Set up monitoring and logging

### Kubernetes Deployment
```bash
kubectl apply -f k8s/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

## 🔄 Version History

- **v1.0.0** - Initial release with basic pipeline monitoring
- **v1.1.0** - Added alerting system
- **v1.2.0** - Enhanced metrics and dashboard
- **v1.3.0** - Multi-tool support and webhooks

---

**Note**: This application is designed for monitoring CI/CD pipelines and should be deployed in a secure environment with proper access controls.
