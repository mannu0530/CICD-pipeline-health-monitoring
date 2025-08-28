# CI/CD Pipeline Health Dashboard

A comprehensive web application for monitoring and managing CI/CD pipelines from multiple tools including GitHub Actions, GitLab CI, and Jenkins. The dashboard provides real-time metrics, build monitoring, alerting, and comprehensive reporting.

## 🚀 Features

### Core Functionality
- **Multi-Tool Integration**: Connect to GitHub Actions, GitLab CI, and Jenkins simultaneously
- **Real-time Monitoring**: Live updates of pipeline status, build progress, and metrics
- **Comprehensive Metrics**: Success/failure rates, build times, deployment statistics
- **Advanced Alerting**: Configurable alerts with Slack and email notifications
- **Webhook Processing**: Automatic processing of CI/CD tool webhooks
- **Role-based Access Control**: Secure authentication and authorization

### Integration Features
- **GitHub Actions**: Monitor workflow runs, jobs, and repository activity
- **GitLab CI**: Track pipelines, jobs, and project metrics
- **Jenkins**: Monitor builds, jobs, and queue status
- **Password-based Authentication**: Support for username/password and API tokens
- **Webhook Security**: Signature verification for secure webhook processing

### Dashboard Features
- **Real-time Metrics**: Live updates of pipeline and build statistics
- **Interactive Charts**: Visual representation of trends and performance
- **Build Logs**: Access to detailed build logs and artifacts
- **Alert Management**: Create, acknowledge, and resolve alerts
- **Configuration Management**: Centralized settings for all integrations

## 🏗️ Architecture

### Backend (Python Flask)
- **Framework**: Flask with Flask-RESTful API
- **Database**: MongoDB for primary data storage
- **Cache**: Redis for session management and caching
- **Authentication**: JWT-based authentication system
- **Services**: Modular service architecture for integrations
- **Webhooks**: Secure webhook processing with signature verification

### Frontend (React)
- **Framework**: React with TypeScript
- **UI Library**: Material-UI components
- **Charts**: Recharts for data visualization
- **State Management**: React hooks and context
- **Routing**: React Router for navigation
- **Real-time Updates**: WebSocket integration for live data

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **Reverse Proxy**: Nginx for production deployment
- **Monitoring**: Built-in health checks and metrics
- **Security**: CORS, rate limiting, and secure headers

## 🛠️ Technology Stack

### Backend
- Python 3.9+
- Flask 2.3.3
- PyMongo 4.5.0
- Redis 5.0.1
- Celery 5.3.4
- PyJWT 2.8.0
- Requests 2.31.0

### Frontend
- React 18
- TypeScript 4.9.5
- Material-UI 5
- Recharts 2.8
- Axios for HTTP requests

### Infrastructure
- MongoDB 6.0
- Redis 7-alpine
- Docker & Docker Compose
- Nginx

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- Modern web browser
- For local development: Python 3.9+, Node.js 18+

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cicd
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Set up your GitHub, GitLab, and Jenkins credentials
```

### 3. Start the Application
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Dashboard
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## ⚙️ Configuration

### GitHub Integration
```bash
# Set in .env file
GITHUB_USERNAME=your-username
GITHUB_PASSWORD=your-personal-access-token
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_BASE_URL=https://api.github.com
```

### GitLab Integration
```bash
# Set in .env file
GITLAB_USERNAME=your-username
GITLAB_PASSWORD=your-personal-access-token
GITLAB_WEBHOOK_SECRET=your-webhook-secret
GITLAB_BASE_URL=https://gitlab.com
```

### Jenkins Integration
```bash
# Set in .env file
JENKINS_URL=http://your-jenkins-url
JENKINS_USERNAME=your-username
JENKINS_API_TOKEN=your-api-token
```

### Slack Integration
```bash
# Set in .env file
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL_ID=C1234567890
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `POST /api/v1/auth/logout` - User logout

### Integrations
- `POST /api/v1/config/integrations/github` - Setup GitHub integration
- `POST /api/v1/config/integrations/gitlab` - Setup GitLab integration
- `POST /api/v1/config/integrations/jenkins` - Setup Jenkins integration
- `GET /api/v1/config/integrations/status` - Get integration status
- `POST /api/v1/config/integrations/test` - Test all integrations

### Pipelines
- `GET /api/v1/pipelines/` - List all pipelines
- `GET /api/v1/pipelines/<id>` - Get pipeline details
- `GET /api/v1/pipelines/<id>/jobs` - Get pipeline jobs

### Builds
- `GET /api/v1/builds/` - List all builds
- `GET /api/v1/builds/<id>` - Get build details
- `GET /api/v1/builds/<id>/logs` - Get build logs

### Metrics
- `GET /api/v1/metrics/` - Get dashboard metrics
- `GET /api/v1/metrics/pipelines` - Get pipeline metrics
- `GET /api/v1/metrics/builds` - Get build metrics
- `GET /api/v1/metrics/trends` - Get trend metrics

### Alerts
- `GET /api/v1/alerts/` - List all alerts
- `POST /api/v1/alerts/` - Create new alert
- `PUT /api/v1/alerts/<id>` - Update alert
- `POST /api/v1/alerts/<id>/acknowledge` - Acknowledge alert
- `POST /api/v1/alerts/<id>/resolve` - Resolve alert

### Webhooks
- `POST /api/v1/webhooks/github` - GitHub webhook endpoint
- `POST /api/v1/webhooks/gitlab` - GitLab webhook endpoint
- `POST /api/v1/webhooks/jenkins` - Jenkins webhook endpoint
- `POST /api/v1/webhooks/test` - Test webhook endpoint

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Webhook Verification**: HMAC signature verification for GitHub and GitLab
- **CORS Protection**: Configurable cross-origin resource sharing
- **Rate Limiting**: API rate limiting to prevent abuse
- **Secure Headers**: Security headers for production deployment
- **Input Validation**: Comprehensive input validation and sanitization

## 📊 Dashboard Features

### Main Dashboard
- **Real-time Metrics**: Live updates of pipeline and build statistics
- **Service Status**: Integration connection status and health
- **Recent Activity**: Latest pipeline runs and build activities
- **Quick Actions**: Quick access to common functions

### Pipelines Panel
- **Pipeline List**: View all pipelines from connected services
- **Status Overview**: Visual representation of pipeline health
- **Filtering**: Filter by service, status, and time range
- **Details View**: Comprehensive pipeline information

### Builds Panel
- **Build History**: Complete build history with status tracking
- **Log Access**: Direct access to build logs and artifacts
- **Build Details**: Comprehensive build information and metadata
- **Real-time Updates**: Live build status updates

### Metrics Panel
- **Performance Charts**: Visual representation of trends and metrics
- **Success Rates**: Success/failure rate analysis
- **Build Times**: Average build time tracking and analysis
- **Export Functionality**: Export metrics data for external analysis

### Alerts Panel
- **Alert Management**: Create, manage, and resolve alerts
- **Alert Rules**: Configurable alert rules and conditions
- **Notification Settings**: Configure Slack and email notifications
- **Alert History**: Complete alert history and resolution tracking

### Configuration Panel
- **Integration Setup**: Configure GitHub, GitLab, and Jenkins connections
- **Authentication**: Manage user accounts and permissions
- **System Settings**: Configure dashboard behavior and appearance
- **Webhook Configuration**: Set up webhook endpoints and secrets

## 🚀 Working Features

### ✅ Fully Functional
- **Authentication System**: Complete login/logout functionality
- **Integration Management**: Setup, test, and manage CI/CD tool connections
- **Real-time Data**: Live updates from connected services
- **Webhook Processing**: Automatic processing of CI/CD tool webhooks
- **Alert System**: Complete alert creation, management, and resolution
- **Metrics Collection**: Real-time metrics from all connected services
- **Build Monitoring**: Comprehensive build tracking and log access
- **Pipeline Management**: Complete pipeline monitoring and management

### 🔧 Configuration Options
- **GitHub**: Username/password or personal access token authentication
- **GitLab**: Username/password or personal access token authentication
- **Jenkins**: Username/API token authentication
- **Slack**: Bot token and webhook URL configuration
- **Email**: SMTP configuration for email notifications
- **Security**: Webhook secrets and JWT configuration

## 🐳 Docker Commands

### Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Production
```bash
# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## 🧪 Testing

### Backend Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Run with coverage
python -m pytest --cov=app tests/
```

### Frontend Testing
```bash
# Run frontend tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

### Integration Testing
```bash
# Test API endpoints
curl -X GET http://localhost:5000/api/v1/health

# Test webhook endpoints
curl -X POST http://localhost:5000/api/v1/webhooks/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## 📈 Monitoring & Health Checks

- **Health Endpoint**: `/api/v1/health` for service health monitoring
- **Metrics Endpoint**: `/api/v1/metrics` for performance metrics
- **Service Status**: Integration connection status monitoring
- **Log Aggregation**: Centralized logging for all services
- **Error Tracking**: Comprehensive error logging and monitoring

## 🔄 Webhook Setup

### GitHub Webhook
1. Go to your repository settings
2. Navigate to Webhooks
3. Add webhook with URL: `http://your-domain/api/v1/webhooks/github`
4. Set content type to `application/json`
5. Add your webhook secret to the dashboard configuration

### GitLab Webhook
1. Go to your project settings
2. Navigate to Webhooks
3. Add webhook with URL: `http://your-domain/api/v1/webhooks/gitlab`
4. Set the webhook token in your dashboard configuration

### Jenkins Webhook
1. Install the Generic Webhook Trigger plugin
2. Configure your job to trigger on webhook
3. Set the webhook URL: `http://your-domain/api/v1/webhooks/jenkins`

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Set up reverse proxy (Nginx)
# Configure SSL certificates
# Set up monitoring and logging
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Scale deployments
kubectl scale deployment backend --replicas=3
kubectl scale deployment frontend --replicas=2
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the docs/ directory for detailed documentation
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join discussions in GitHub Discussions
- **Wiki**: Check the project wiki for additional resources

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Password-based authentication for GitHub, GitLab, and Jenkins
- ✅ Fully functional dashboard with real-time data
- ✅ Complete webhook processing and alerting system
- ✅ Comprehensive metrics and reporting
- ✅ Production-ready architecture and security

### v1.0.0
- ✅ Basic dashboard structure
- ✅ Docker containerization
- ✅ MongoDB integration
- ✅ React frontend with Material-UI

## 🎯 Roadmap

- [ ] Advanced analytics and machine learning insights
- [ ] Multi-tenant support
- [ ] Advanced notification channels (Teams, Discord, etc.)
- [ ] Custom dashboard widgets
- [ ] API rate limiting and usage analytics
- [ ] Advanced security features (2FA, SSO)
- [ ] Mobile application
- [ ] Integration with additional CI/CD tools
