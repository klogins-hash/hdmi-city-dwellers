#!/bin/bash

# HDMI City Dwellers Deployment Script
# Deploy to server: 2604:a880:800:14:0:1:b374:e000

SERVER="2604:a880:800:14:0:1:b374:e000"
PROJECT_NAME="hdmi-city-dwellers"
REMOTE_PATH="/opt/$PROJECT_NAME"

echo "🚀 Deploying HDMI City Dwellers to server: $SERVER"

# Check if server is reachable
echo "📡 Testing server connectivity..."
if ! ping -c 1 "$SERVER" > /dev/null 2>&1; then
    echo "❌ Server $SERVER is not reachable"
    exit 1
fi

echo "✅ Server is reachable"

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf hdmi-city-dwellers.tar.gz \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.env' \
    .

echo "✅ Deployment package created"

# Copy files to server
echo "📤 Copying files to server..."
scp hdmi-city-dwellers.tar.gz root@[$SERVER]:~/

# Connect to server and deploy
echo "🔧 Deploying on server..."
ssh root@[$SERVER] << 'EOF'
    # Install Docker if not present
    if ! command -v docker &> /dev/null; then
        echo "🐳 Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl start docker
        systemctl enable docker
    fi

    # Install Docker Compose if not present
    if ! command -v docker-compose &> /dev/null; then
        echo "🐙 Installing Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi

    # Create project directory
    mkdir -p /opt/hdmi-city-dwellers
    cd /opt/hdmi-city-dwellers

    # Extract files
    tar -xzf ~/hdmi-city-dwellers.tar.gz

    # Create environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️  Please edit .env file with your API keys:"
        echo "   - WEAVIATE_API_KEY"
        echo "   - OPENAI_API_KEY"
    fi

    # Build and start services
    echo "🏗️  Building and starting services..."
    docker-compose down || true
    docker-compose build
    docker-compose up -d

    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 30

    # Check service status
    echo "📊 Service status:"
    docker-compose ps

    echo "✅ Deployment complete!"
    echo "🌐 Application should be available at:"
    echo "   Frontend: http://[$SERVER]:3000"
    echo "   Backend API: http://[$SERVER]:8000"
    echo "   Health Check: http://[$SERVER]:8000/health"
EOF

# Cleanup local deployment package
rm hdmi-city-dwellers.tar.gz

echo "🎉 Deployment script completed!"
echo ""
echo "📋 Next steps:"
echo "1. SSH to server: ssh root@[$SERVER]"
echo "2. Edit environment: nano /opt/hdmi-city-dwellers/.env"
echo "3. Add your API keys (WEAVIATE_API_KEY, OPENAI_API_KEY)"
echo "4. Restart services: cd /opt/hdmi-city-dwellers && docker-compose restart"
echo "5. Setup sample data: python scripts/setup_hdmi_data.py"
echo "6. Access application: http://[$SERVER]:3000"
