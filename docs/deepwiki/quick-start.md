# Quick Start Guide

Get CultivAR running in 5 minutes with this streamlined setup guide.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Option 1: Local Development Setup (Recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/jluna0413/CultivAREmergent.git
cd CultivAREmergent

# Install dependencies
pip install -r requirements.txt
```

### 2. Quick Configuration

```bash
# Set minimal environment variables
export SECRET_KEY="your-secret-key-here"
export CULTIVAR_DB_DRIVER="sqlite"
export DEBUG="true"
```

### 3. Initialize Database

```bash
# Create database and add sample data
python -c "
from cultivar_app import create_app
from app.models import db, init_db, migrate_db
app = create_app()
with app.app_context():
    migrate_db()
    init_db()
print('Database initialized successfully!')
"
```

### 4. Start the Application

```bash
# Start the main application
python cultivar_app.py
```

### 5. Access CultivAR

Open your browser and navigate to:
- **Main Application**: http://localhost:5000
- **Default Login**: 
  - Username: `admin`
  - Password: `isley`

## Option 2: Docker Quick Start

```bash
# Clone repository
git clone https://github.com/jluna0413/CultivAREmergent.git
cd CultivAREmergent

# Start with Docker Compose
docker-compose -f docker-compose.sqlite.yml up -d

# Access at http://localhost:5000
```

## Option 3: AI Integration Quick Start

### Enable MCP (Model Context Protocol)

```bash
# Install MCP dependencies
pip install mcp

# Start with MCP enabled
export CULTIVAR_MCP_ENABLED=true
python cultivar_app.py --enable-mcp
```

### Configure AI Assistant

Add to your AI assistant configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "cultivar": {
      "command": "python",
      "args": ["/path/to/CultivAREmergent/mcp_server.py"]
    }
  }
}
```

## Verification Steps

### 1. Test Web Interface
- ✅ Login page loads at http://localhost:5000
- ✅ Can login with default credentials
- ✅ Dashboard displays without errors

### 2. Test Database
```bash
# Quick database test
python -c "
from cultivar_app import create_app
from app.models.base_models import User
app = create_app()
with app.app_context():
    users = User.query.all()
    print(f'Found {len(users)} users in database')
"
```

### 3. Test MCP Integration (if enabled)
```bash
# Test MCP server
python mcp_server.py &
# Should start without errors
```

## What's Next?

### Essential First Steps
1. **Change Default Password**: Go to Settings → Account → Change Password
2. **Add Your First Plant**: Navigate to Plants → Add New Plant
3. **Explore Features**: Check out strain database, environmental monitoring

### Documentation
- 📖 [User Guide](user-guide.md) - Complete feature walkthrough
- 🔧 [Configuration](configuration.md) - Detailed configuration options
- 🤖 [MCP Integration](mcp-integration.md) - AI assistant setup

### Support
- 🐛 [Report Issues](https://github.com/jluna0413/CultivAREmergent/issues)
- 💬 [Community Discussion](https://github.com/jluna0413/CultivAREmergent/discussions)

## Troubleshooting Quick Fixes

### Common Issues

**Database Error**
```bash
# Reset database
rm -f data/cultivar.db
python -c "from cultivar_app import create_app; from app.models import migrate_db, init_db; app = create_app(); migrate_db(); init_db()"
```

**Port Already in Use**
```bash
# Use different port
export CULTIVAR_PORT=5001
python cultivar_app.py
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

🚀 **You're ready to start growing with CultivAR!**

## 🔗 See Also

- [Installation Guide](installation.md) - Detailed installation options
- [User Guide](user-guide.md) - Complete user manual
- [Troubleshooting](troubleshooting.md) - Comprehensive troubleshooting guide