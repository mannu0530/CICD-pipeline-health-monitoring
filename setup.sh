#!/bin/bash

# CI/CD Pipeline Health Dashboard Setup Script

echo "🚀 Setting up CI/CD Pipeline Health Dashboard..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your configuration before running the application"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p scripts
mkdir -p nginx/ssl

# Create MongoDB initialization script
echo "📝 Creating MongoDB initialization script..."
cat > scripts/init-mongo.js << 'EOF'
db = db.getSiblingDB('cicd_dashboard');

// Create collections
db.createCollection('pipelines');
db.createCollection('builds');
db.createCollection('metrics');
db.createCollection('alerts');
db.createCollection('configurations');

// Create indexes
db.pipelines.createIndex({ "pipeline_id": 1 }, { unique: true });
db.pipelines.createIndex({ "tool": 1, "status": 1 });
db.pipelines.createIndex({ "started_at": -1 });

db.builds.createIndex({ "build_id": 1 }, { unique: true });
db.builds.createIndex({ "pipeline_id": 1 });
db.builds.createIndex({ "status": 1, "started_at": -1 });

db.metrics.createIndex({ "date": 1, "tool": 1 }, { unique: true });

db.alerts.createIndex({ "status": 1, "created_at": -1 });

print('MongoDB initialized successfully');
EOF

# Create nginx configuration
echo "📝 Creating nginx configuration..."
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    upstream backend {
        server backend:5000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health checks
        location /health {
            proxy_pass http://backend;
        }
    }
}
EOF

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'docker-compose up -d' to start the application"
echo "3. Access the dashboard at http://localhost:3000"
echo "4. Access the API at http://localhost:5000"
echo ""
echo "🔧 Useful commands:"
echo "  docker-compose up -d          # Start all services"
echo "  docker-compose logs -f        # View logs"
echo "  docker-compose down           # Stop all services"
echo "  docker-compose restart        # Restart all services"
echo ""
echo "📚 For more information, see README.md"
