# CultivAR

CultivAR is a self-hosted cannabis grow journal application with AI integration. It allows you to track your plants, strains, and environmental data, now enhanced with Model Context Protocol (MCP) support for intelligent AI assistance.

## ✨ New Features

### 🤖 AI Integration via MCP
- **Model Context Protocol (MCP)** support for AI assistants
- **Claude Desktop integration** for intelligent grow assistance  
- **Natural language queries** about your grow data
- **Automated activity logging** through AI commands
- **Smart insights and recommendations**

### 📚 Enhanced Documentation
- **DeepWiki documentation system** with comprehensive guides
- **Interactive API reference** with examples
- **Architecture documentation** for developers
- **AI assistant setup guides**

## Features

- Plant tracking (growth stages, activities, measurements)
- Strain management with comprehensive database
- Sensor integration (AC Infinity, Ecowitt)
- Image uploads and timeline tracking
- Environmental data visualization
- User authentication and security
- **🆕 AI Assistant integration via MCP**
- **🆕 Comprehensive deepwiki documentation**

## Quick Start

### Option 1: Easy Launch (Recommended)

```bash
# Clone the repository
git clone https://github.com/jluna0413/CultivAREmergent.git
cd CultivAREmergent

# Install dependencies
pip install -r requirements.txt

# Launch with AI integration
python launch_cultivar.py --mode both

# Access at http://localhost:5000
# Default login: admin / isley
```

### Option 2: AI-Only Mode

```bash
# Start just the MCP server for AI integration
python launch_cultivar.py --mode mcp

# Configure your AI assistant to connect to localhost:8001
```

### Option 3: Traditional Setup

```bash
# Traditional Flask app only
python launch_cultivar.py --mode app
```

## AI Assistant Setup

### Claude Desktop Integration

1. **Add to Claude Desktop config** (`~/.config/claude-desktop/config.json`):

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

2. **Start CultivAR with MCP:**
```bash
python launch_cultivar.py --mode both
```

3. **Use natural language in Claude:**
```
"Show me all my active plants and their current growth stage"
"Record that I watered Plant #1 with 500ml today"
"What are the current environmental conditions?"
```

## Documentation

### 📖 Complete Documentation
- **[DeepWiki Documentation](docs/deepwiki/README.md)** - Comprehensive documentation system
- **[Quick Start Guide](docs/deepwiki/quick-start.md)** - Get running in 5 minutes  
- **[AI Assistant Setup](docs/deepwiki/ai-assistant-setup.md)** - Configure AI integration
- **[MCP Integration](docs/deepwiki/mcp-integration.md)** - Complete MCP reference
- **[API Reference](docs/deepwiki/api-reference.md)** - Full API documentation
- **[Architecture Guide](docs/deepwiki/architecture.md)** - System architecture

### 🚀 Getting Started
- [Installation Guide](docs/wiki/Installation.md) - Detailed installation
- [User Guide](docs/wiki/User-Guide.md) - Feature walkthrough
- [Developer Guide](docs/wiki/Developer-Guide.md) - Development setup

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- SQLite or PostgreSQL

### Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/jluna0413/CultivAREmergent.git
   cd CultivAREmergent
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python launch_cultivar.py
   ```

4. Access the application at http://localhost:5000

### Docker Installation

#### SQLite Version
```bash
docker-compose -f docker-compose.sqlite.yml up -d
```

#### PostgreSQL Version  
```bash
docker-compose -f docker-compose.postgres.yml up -d
```

## Default Credentials

- Username: admin
- Password: isley

**Important:** Change the default password after first login.

## Configuration

CultivAR can be configured using environment variables:

### Core Configuration
- `SECRET_KEY`: Secret key for session management
- `CULTIVAR_DB_DRIVER`: Database driver (`sqlite` or `postgres`)
- `CULTIVAR_PORT`: Application port (default: `5000`)
- `DEBUG`: Debug mode (`true` or `false`)

### AI/MCP Configuration
- `CULTIVAR_MCP_ENABLED`: Enable MCP server (`true` or `false`)
- `CULTIVAR_MCP_PORT`: MCP server port (default: `8001`)
- `CULTIVAR_MCP_HOST`: MCP server host (default: `127.0.0.1`)

### Database Configuration (PostgreSQL)
- `CULTIVAR_DB_HOST`: PostgreSQL host (default: `localhost`)
- `CULTIVAR_DB_PORT`: PostgreSQL port (default: `5432`)
- `CULTIVAR_DB_USER`: PostgreSQL username (default: `cultivar`)
- `CULTIVAR_DB_PASSWORD`: PostgreSQL password (default: `cultivar`)
- `CULTIVAR_DB_NAME`: PostgreSQL database name (default: `cultivardb`)

## Testing

Run the integration test suite:

```bash
python test_integration.py
```

This tests:
- ✅ Documentation completeness
- ✅ CultivAR application startup
- ✅ MCP server functionality
- ✅ AI integration capabilities

## What's New in This Release

### 🤖 AI Integration
- **Model Context Protocol (MCP) support** - Industry-standard AI integration
- **6 intelligent tools** for AI assistants to interact with grow data
- **Natural language plant management** - Ask questions, get answers
- **Automated activity logging** via AI commands

### 📚 Enhanced Documentation  
- **DeepWiki system** - Interconnected, comprehensive documentation
- **Interactive examples** with copy-paste code snippets
- **Architecture guides** for developers and integrators
- **AI setup tutorials** for popular assistants

### 🚀 Improved Developer Experience
- **Integrated launcher** (`launch_cultivar.py`) with multiple modes
- **Comprehensive testing** with `test_integration.py`
- **Better error handling** and logging
- **Enhanced configuration** management

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project is a Python port of the [Isley](https://github.com/dwot/isley) project by dwot, enhanced with modern AI integration capabilities.

## Support

- 🐛 [Report Issues](https://github.com/jluna0413/CultivAREmergent/issues)
- 💡 [Request Features](https://github.com/jluna0413/CultivAREmergent/issues)  
- 💬 [Join Discussions](https://github.com/jluna0413/CultivAREmergent/discussions)
- 📚 [Read the Docs](docs/deepwiki/README.md)
