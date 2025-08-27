# Quick Start Guide - CI/CD Pipeline Health Dashboard

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd cicd

# Run the setup script
./setup.sh
```

### 2. Configure Environment
```bash
# Edit the environment file
nano .env

# Key configurations to update:
# - MONGODB_URI (if using external MongoDB)
# - SLACK_BOT_TOKEN (for Slack notifications)
# - SMTP settings (for email notifications)
```

### 3. Start the Application
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

### 5. Verify Installation
```bash
# Check health endpoints
curl http://localhost:5000/health
curl http://localhost:3000/health

# Check MongoDB connection
docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"
```

## 🔧 Development Mode

### Backend Development
```bash
# Enter backend container
docker-compose exec backend bash

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
python app.py
```

### Frontend Development
```bash
# Enter frontend container
docker-compose exec frontend sh

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 First Steps

1. **View Dashboard**: Navigate to http://localhost:3000
2. **Check Metrics**: View the main dashboard with sample data
3. **Explore Navigation**: Use the sidebar to navigate between sections
4. **Configure Integrations**: Set up CI/CD tool webhooks

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000
lsof -i :5000

# Stop conflicting services or change ports in docker-compose.yml
```

#### MongoDB Connection Issues
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

#### Frontend Build Issues
```bash
# Clear node modules and reinstall
docker-compose exec frontend rm -rf node_modules package-lock.json
docker-compose exec frontend npm install
```

### Logs and Debugging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Enter containers for debugging
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec mongodb mongosh
```

## 🚀 Production Deployment

### 1. Update Environment
```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=false

# Update .env file with production values
nano .env
```

### 2. Build and Deploy
```bash
# Build production images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. SSL Configuration
```bash
# Add SSL certificates to nginx/ssl/
# Update nginx configuration for HTTPS
# Restart nginx service
```

## 📚 Next Steps

1. **Read Documentation**: Review README.md and technical documents
2. **Configure CI/CD Tools**: Set up webhooks for GitHub, GitLab, Jenkins
3. **Customize Alerts**: Configure Slack and email notifications
4. **Monitor Performance**: Check metrics and optimize as needed
5. **Scale Infrastructure**: Add load balancers and monitoring

## 🆘 Need Help?

- Check the logs: `docker-compose logs -f`
- Review configuration files
- Check network connectivity between services
- Verify environment variables are set correctly

## 🔄 Updates and Maintenance

```bash
# Update application
git pull origin main
docker-compose down
docker-compose up -d --build

# Backup database
docker-compose exec mongodb mongodump --out /backup

# Restore database
docker-compose exec mongodb mongorestore /backup
```

---

**Happy Monitoring! 🎉**
