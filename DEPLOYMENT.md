# HDMI City Dwellers - Automated Deployment Guide

This guide sets up automated deployment from GitHub to your server at `2604:a880:800:14:0:1:b374:e000`.

## 🚀 Quick Setup

### 1. Initial Server Setup

SSH to your server and run the setup script:

```bash
ssh root@2604:a880:800:14:0:1:b374:e000
wget https://raw.githubusercontent.com/YOUR_USERNAME/hdmi-city-dwellers/main/server-setup.sh
chmod +x server-setup.sh
./server-setup.sh
```

### 2. Clone Repository

```bash
cd /opt/hdmi-city-dwellers
git clone https://github.com/YOUR_USERNAME/hdmi-city-dwellers.git .
```

### 3. Configure Environment

```bash
nano .env
```

Add your API keys:
```bash
WEAVIATE_API_KEY=your-actual-weaviate-key
OPENAI_API_KEY=your-actual-openai-key
ENVIRONMENT=production
LOG_LEVEL=info
```

### 4. Start Services

```bash
docker-compose up -d
```

### 5. Setup GitHub Secrets

In your GitHub repository, go to Settings → Secrets and variables → Actions, and add:

- `SSH_PRIVATE_KEY`: Private key content from server (see setup script output)
- `SERVER_HOST`: `2604:a880:800:14:0:1:b374:e000`
- `SERVER_USER`: `root`

## 🔄 How Automated Deployment Works

1. **Push to GitHub**: When you push to `main` or `master` branch
2. **GitHub Actions Triggers**: Workflow starts automatically
3. **Build & Deploy**: Code is packaged and deployed to server
4. **Service Restart**: Docker containers are rebuilt and restarted
5. **Health Check**: System verifies deployment success

## 📊 Monitoring

### Check Deployment Status
- GitHub Actions tab in your repository
- Server logs: `ssh root@2604:a880:800:14:0:1:b374:e000 "cd /opt/hdmi-city-dwellers && docker-compose logs"`

### Access Application
- Frontend: `http://2604:a880:800:14:0:1:b374:e000:3000`
- Backend API: `http://2604:a880:800:14:0:1:b374:e000:8000`
- Health Check: `http://2604:a880:800:14:0:1:b374:e000:8000/health`

### Service Management
```bash
# SSH to server
ssh root@2604:a880:800:14:0:1:b374:e000

# Check status
cd /opt/hdmi-city-dwellers
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Start services
docker-compose up -d
```

## 🔧 Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs
2. SSH to server and check Docker logs
3. Verify environment variables are set
4. Ensure server has enough resources

### Services Won't Start
1. Check Docker logs: `docker-compose logs`
2. Verify API keys in `.env` file
3. Check port availability: `netstat -tlnp | grep :3000`
4. Restart Docker: `systemctl restart docker`

### Can't Access Application
1. Check firewall: `ufw status`
2. Verify services are running: `docker-compose ps`
3. Test health endpoint: `curl localhost:8000/health`

## 🔒 Security Notes

- Server uses non-root Docker containers
- Firewall configured for necessary ports only
- SSH key authentication for deployments
- Environment variables stored securely
- Regular security updates via automated deployment

## 📝 Making Changes

1. Edit code locally
2. Commit and push to GitHub
3. GitHub Actions automatically deploys
4. Monitor deployment in Actions tab
5. Verify changes on server

That's it! Every push to your main branch will now automatically update your server.
