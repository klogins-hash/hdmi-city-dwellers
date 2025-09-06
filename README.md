# HDMI City Dwellers

Urban Technology Knowledge Base - AI-powered system for managing smart city infrastructure and connectivity knowledge.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo>
cd hdmi-city-dwellers

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# WEAVIATE_API_KEY=your-secret-key
# OPENAI_API_KEY=your-openai-key

# Build and start everything
docker-compose up -d

# Wait for services to be ready (check logs)
docker-compose logs -f

# Setup sample data
python scripts/setup_hdmi_data.py

# Access the application
open http://localhost:3000
```

## 📁 Project Structure

```
hdmi-city-dwellers/
├── README.md
├── docker-compose.yml
├── .env.example
├── .env
├── .gitignore
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── weaviate_manager.py
│   └── chat_processor.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── App.js
│   │   ├── Chat.js
│   │   └── App.css
│   └── public/
│       └── index.html
└── scripts/
    └── setup_hdmi_data.py
```

## 🏙️ Features

- **AI-Powered Chat Interface**: Natural language interaction with urban technology knowledge
- **Smart Knowledge Management**: Add, update, delete, and search urban infrastructure data
- **Category Organization**: Technology, smart-city, infrastructure, urban-planning, connectivity
- **Real-time Statistics**: Database metrics and performance monitoring
- **Responsive Design**: Works on desktop and mobile devices
- **Docker Deployment**: Easy containerized deployment

## 🔧 Technology Stack

- **Backend**: FastAPI + Python 3.11
- **Frontend**: React 18 + Modern CSS
- **Database**: Weaviate Vector Database
- **Cache**: Redis
- **AI**: OpenAI GPT for embeddings and generation
- **Deployment**: Docker + Docker Compose

## 🎯 Usage Examples

### Search Queries
- `"What is HDMI 2.1?"`
- `"Tell me about smart city infrastructure"`
- `"How do urban displays work?"`

### Database Management
- `add: LED Street Lighting | Smart LED systems for energy-efficient urban lighting | infrastructure`
- `delete: HDMI 2.1`
- `update: Smart City Display Networks | Enhanced description with new features`
- `list technology`
- `list all`
- `stats`

### Quick Commands
- `help` - Show all available commands
- `clear` - Clear cache
- `stats` - Show database statistics

## 🌟 Categories

- **technology**: HDMI standards, display tech, connectivity solutions
- **smart-city**: Urban intelligence, IoT integration, city-wide systems
- **infrastructure**: Physical systems, networks, installations
- **urban-planning**: City design, traffic management, public spaces
- **connectivity**: Network solutions, data transmission, integration

## 🚀 Deployment to Server

To deploy to your server at `2604:a880:800:14:0:1:b374:e000`:

1. **Prepare the server** (ensure Docker and Docker Compose are installed)
2. **Transfer files** to the server
3. **Configure environment** variables
4. **Deploy** using Docker Compose

## 📊 Performance

| Operation | Expected Time | Notes |
|-----------|--------------|-------|
| Search Query | < 100ms | Cached results < 20ms |
| Add Knowledge | < 200ms | Includes vectorization |
| Delete/Update | < 150ms | Direct database operation |
| List Commands | < 80ms | Simple retrieval |

## 🔒 Security

- Non-root Docker containers
- API key authentication for Weaviate
- CORS protection
- Input validation and sanitization

## 🛠️ Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm start
```

## 📝 License

MIT License - Feel free to use for urban technology projects!

---

**HDMI City Dwellers** - Connecting urban environments through intelligent infrastructure management.
