# HDMI City Dwellers - Final Setup Instructions

## 🎯 Repository Created Successfully!
**GitHub Repository**: https://github.com/klogins-hash/hdmi-city-dwellers

## 🚀 Next Steps for Automated Deployment

### 1. Set up GitHub Secrets

Go to your repository: https://github.com/klogins-hash/hdmi-city-dwellers/settings/secrets/actions

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `SSH_PRIVATE_KEY` | SSH private key from your server (see step 2) |
| `SERVER_HOST` | `2604:a880:800:14:0:1:b374:e000` |
| `SERVER_USER` | `root` |

### 2. Server Setup (Run Once)

SSH to your server and run the setup:

```bash
ssh root@2604:a880:800:14:0:1:b374:e000

# Download and run setup script
curl -O https://raw.githubusercontent.com/klogins-hash/hdmi-city-dwellers/main/server-setup.sh
chmod +x server-setup.sh
./server-setup.sh

# Generate SSH key for GitHub Actions
ssh-keygen -t ed25519 -f ~/.ssh/hdmi_deploy -N ''
cat ~/.ssh/hdmi_deploy.pub >> ~/.ssh/authorized_keys

# Copy this private key content for GitHub Secrets
cat ~/.ssh/hdmi_deploy
```

### 3. Clone Repository on Server

```bash
cd /opt/hdmi-city-dwellers
git clone https://github.com/klogins-hash/hdmi-city-dwellers.git .
```

### 4. Configure Environment

```bash
nano .env
```

Add your API keys:
```
WEAVIATE_API_KEY=your-actual-weaviate-key
OPENAI_API_KEY=your-actual-openai-key
ENVIRONMENT=production
LOG_LEVEL=info
```

### 5. Start Services

```bash
docker-compose up -d
```

### 6. Test Deployment

```bash
# Check health
curl http://localhost:8000/health

# Setup sample data
python scripts/setup_hdmi_data.py
```

## 🔄 How Automated Deployment Works

1. **Push to GitHub** → GitHub Actions triggers
2. **Builds and deploys** to your server automatically  
3. **Health checks** ensure successful deployment
4. **Access your app** at: http://2604:a880:800:14:0:1:b374:e000:3000

## 🎉 You're All Set!

Once you complete the server setup and add the GitHub Secrets, every push to the `main` branch will automatically deploy to your server!

**Repository**: https://github.com/klogins-hash/hdmi-city-dwellers
**Frontend**: http://2604:a880:800:14:0:1:b374:e000:3000
**Backend API**: http://2604:a880:800:14:0:1:b374:e000:8000
