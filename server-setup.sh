#!/bin/bash

# HDMI City Dwellers - Initial Server Setup Script
# Run this ONCE on your server: 2604:a880:800:14:0:1:b374:e000

SERVER_HOST="2604:a880:800:14:0:1:b374:e000"
PROJECT_NAME="hdmi-city-dwellers"
PROJECT_PATH="/opt/$PROJECT_NAME"

echo "🏙️ HDMI City Dwellers - Server Setup"
echo "Setting up server: $SERVER_HOST"

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "🐙 Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose already installed"
fi

# Install Git
if ! command -v git &> /dev/null; then
    echo "📚 Installing Git..."
    apt install -y git
else
    echo "✅ Git already installed"
fi

# Create project directory
echo "📁 Creating project directory..."
mkdir -p $PROJECT_PATH
cd $PROJECT_PATH

# Clone repository (you'll need to update this URL)
echo "📥 Cloning repository..."
echo "⚠️  You need to run this command manually with your GitHub repo URL:"
echo "    git clone https://github.com/YOUR_USERNAME/hdmi-city-dwellers.git ."
echo ""

# Create environment file template
echo "⚙️ Creating environment configuration..."
cat > .env << 'EOF'
# HDMI City Dwellers Environment Configuration
# IMPORTANT: Add your actual API keys below

WEAVIATE_API_KEY=your-weaviate-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here

# App Settings
ENVIRONMENT=production
LOG_LEVEL=info
EOF

# Set up firewall rules
echo "🔥 Configuring firewall..."
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3000/tcp  # Frontend
ufw allow 8000/tcp  # Backend API
ufw --force enable

# Create systemd service for auto-start
echo "🚀 Creating systemd service..."
cat > /etc/systemd/system/hdmi-city-dwellers.service << EOF
[Unit]
Description=HDMI City Dwellers
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_PATH
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable hdmi-city-dwellers

# Create deployment user (optional, for better security)
echo "👤 Creating deployment user..."
useradd -m -s /bin/bash deploy || true
usermod -aG docker deploy || true

# Set up SSH key for GitHub Actions
echo "🔑 SSH Key Setup for GitHub Actions"
echo "1. Generate SSH key pair:"
echo "   ssh-keygen -t ed25519 -f ~/.ssh/hdmi_deploy -N ''"
echo ""
echo "2. Add public key to authorized_keys:"
echo "   cat ~/.ssh/hdmi_deploy.pub >> ~/.ssh/authorized_keys"
echo ""
echo "3. Copy private key content for GitHub Secrets:"
echo "   cat ~/.ssh/hdmi_deploy"
echo ""

# Display next steps
echo ""
echo "🎉 Server setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Clone your repository:"
echo "   cd $PROJECT_PATH"
echo "   git clone https://github.com/YOUR_USERNAME/hdmi-city-dwellers.git ."
echo ""
echo "2. Edit environment file:"
echo "   nano $PROJECT_PATH/.env"
echo "   # Add your WEAVIATE_API_KEY and OPENAI_API_KEY"
echo ""
echo "3. Start services:"
echo "   docker-compose up -d"
echo ""
echo "4. Set up GitHub Secrets in your repository:"
echo "   - SSH_PRIVATE_KEY: (content of ~/.ssh/hdmi_deploy)"
echo "   - SERVER_HOST: $SERVER_HOST"
echo "   - SERVER_USER: root"
echo ""
echo "5. Test deployment:"
echo "   curl http://$SERVER_HOST:8000/health"
echo "   # Should return healthy status"
echo ""
echo "6. Access application:"
echo "   Frontend: http://$SERVER_HOST:3000"
echo "   Backend: http://$SERVER_HOST:8000"
echo ""
echo "🔄 After GitHub setup, every push to main/master will auto-deploy!"
