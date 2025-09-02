# Model Context Protocol (MCP) Integration

The CultivAR Model Context Protocol integration enables AI assistants and Large Language Models (LLMs) to interact with your grow journal data in a secure, structured way.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows LLMs to access external data sources and capabilities. CultivAR's MCP implementation provides AI assistants with the ability to:

- Read plant data and growth history
- Access strain information and genetics
- Retrieve environmental sensor data
- Help with grow planning and troubleshooting
- Generate reports and insights

## Quick Start

### Prerequisites
- CultivAR server running
- MCP-compatible AI assistant (Claude Desktop, etc.)
- Network access between AI assistant and CultivAR server

### Basic Setup

1. **Enable MCP in CultivAR configuration:**
```bash
export CULTIVAR_MCP_ENABLED=true
export CULTIVAR_MCP_PORT=8001
export CULTIVAR_MCP_HOST=0.0.0.0
```

2. **Start CultivAR with MCP support:**
```bash
python cultivar_app.py --enable-mcp
```

3. **Configure your AI assistant** to connect to the MCP server:
```json
{
  "mcpServers": {
    "cultivar": {
      "command": "stdio",
      "args": ["--server", "http://localhost:8001/mcp"]
    }
  }
}
```

## Available MCP Tools

### Plant Management Tools

#### `get_plants`
Retrieve all plants in the grow journal.

**Parameters:**
- `active_only` (boolean, optional): Only return active plants
- `strain_id` (integer, optional): Filter by strain ID

**Example:**
```json
{
  "name": "get_plants",
  "arguments": {
    "active_only": true
  }
}
```

#### `get_plant_details`
Get detailed information about a specific plant.

**Parameters:**
- `plant_id` (integer, required): Plant ID to retrieve

#### `add_plant_activity`
Record a new activity for a plant.

**Parameters:**
- `plant_id` (integer, required): Target plant ID
- `activity_type` (string, required): Type of activity (watering, feeding, etc.)
- `notes` (string, optional): Activity notes
- `amount` (float, optional): Amount for measurements

### Strain Information Tools

#### `get_strains`
Retrieve strain database information.

**Parameters:**
- `search` (string, optional): Search term for strain names
- `genetics` (string, optional): Filter by genetic type (indica, sativa, hybrid)

#### `get_strain_details`
Get detailed information about a specific strain.

**Parameters:**
- `strain_id` (integer, required): Strain ID to retrieve

### Environmental Data Tools

#### `get_environmental_data`
Retrieve sensor data and environmental conditions.

**Parameters:**
- `start_date` (string, optional): Start date (ISO format)
- `end_date` (string, optional): End date (ISO format)
- `sensor_type` (string, optional): Filter by sensor type

#### `get_grow_room_status`
Get current environmental conditions.

**Returns:**
- Current temperature, humidity, light levels
- Sensor status and connectivity
- Alert conditions

### Analytics and Reporting Tools

#### `generate_grow_report`
Generate comprehensive grow cycle reports.

**Parameters:**
- `plant_id` (integer, optional): Specific plant report
- `date_range` (string, optional): Report period
- `format` (string, optional): Output format (summary, detailed)

#### `get_growth_trends`
Analyze growth patterns and trends.

**Parameters:**
- `metric` (string, required): Metric to analyze (height, yield, etc.)
- `period` (string, optional): Analysis period

## Security and Authentication

### API Key Authentication
MCP requests require authentication via API key:

```json
{
  "headers": {
    "Authorization": "Bearer YOUR_API_KEY"
  }
}
```

### Permission Levels
- **Read-only**: Access to plant data and reports
- **Standard**: Add activities and measurements
- **Admin**: Full access including configuration

### Data Privacy
- All MCP communications are encrypted
- Personal data is filtered from responses
- Audit logs track all MCP interactions

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CULTIVAR_MCP_ENABLED` | `false` | Enable MCP server |
| `CULTIVAR_MCP_PORT` | `8001` | MCP server port |
| `CULTIVAR_MCP_HOST` | `127.0.0.1` | MCP server host |
| `CULTIVAR_MCP_AUTH_REQUIRED` | `true` | Require authentication |
| `CULTIVAR_MCP_LOG_LEVEL` | `INFO` | MCP logging level |

### MCP Server Configuration File

Create `config/mcp_config.json`:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8001,
    "debug": false
  },
  "authentication": {
    "required": true,
    "api_key_header": "Authorization",
    "session_timeout": 3600
  },
  "tools": {
    "plant_management": {
      "enabled": true,
      "read_only": false
    },
    "environmental_data": {
      "enabled": true,
      "historical_limit": "30d"
    },
    "reporting": {
      "enabled": true,
      "max_report_size": "10MB"
    }
  },
  "rate_limiting": {
    "requests_per_minute": 60,
    "burst_limit": 10
  }
}
```

## Usage Examples

### Example 1: Basic Plant Query

**AI Assistant Prompt:**
"Show me all my active plants and their current growth stage"

**MCP Tool Call:**
```json
{
  "name": "get_plants",
  "arguments": {
    "active_only": true
  }
}
```

**Response:**
```json
{
  "plants": [
    {
      "id": 1,
      "name": "Blue Dream #1",
      "strain": "Blue Dream",
      "stage": "flowering",
      "days_in_stage": 42,
      "last_activity": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Purple Haze #2",
      "strain": "Purple Haze",
      "stage": "vegetative",
      "days_in_stage": 28,
      "last_activity": "2024-01-14T16:45:00Z"
    }
  ]
}
```

### Example 2: Environmental Analysis

**AI Assistant Prompt:**
"What were the temperature and humidity levels in my grow room last week?"

**MCP Tool Call:**
```json
{
  "name": "get_environmental_data",
  "arguments": {
    "start_date": "2024-01-08T00:00:00Z",
    "end_date": "2024-01-15T00:00:00Z",
    "sensor_type": "climate"
  }
}
```

### Example 3: Adding Plant Activity

**AI Assistant Prompt:**
"Record that I watered Plant #1 with 500ml of water today"

**MCP Tool Call:**
```json
{
  "name": "add_plant_activity",
  "arguments": {
    "plant_id": 1,
    "activity_type": "watering",
    "amount": 500,
    "notes": "Regular watering schedule"
  }
}
```

## Troubleshooting

### Common Issues

**Connection Refused**
- Check if MCP server is running: `curl http://localhost:8001/mcp/health`
- Verify firewall settings
- Check host/port configuration

**Authentication Errors**
- Verify API key is correct
- Check permission levels
- Review authentication logs

**Tool Not Found**
- Ensure tool is enabled in configuration
- Check spelling of tool names
- Verify MCP server version compatibility

### Debug Mode

Enable debug logging:
```bash
export CULTIVAR_MCP_LOG_LEVEL=DEBUG
```

Check MCP server logs:
```bash
tail -f logs/mcp_server.log
```

## Integration Examples

### Claude Desktop Configuration

Add to Claude Desktop config file (`~/.config/claude-desktop/config.json`):

```json
{
  "mcpServers": {
    "cultivar-grow-journal": {
      "command": "python",
      "args": [
        "/path/to/cultivar/mcp_client.py",
        "--server-url", "http://localhost:8001/mcp",
        "--api-key", "your-api-key-here"
      ],
      "env": {
        "CULTIVAR_API_URL": "http://localhost:5000"
      }
    }
  }
}
```

### Custom LLM Integration

```python
import requests
import json

class CultivARMCPClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def call_tool(self, tool_name, arguments):
        response = requests.post(
            f"{self.base_url}/mcp/tools/{tool_name}",
            json={"arguments": arguments},
            headers=self.headers
        )
        return response.json()

# Usage
client = CultivARMCPClient("http://localhost:8001", "your-api-key")
plants = client.call_tool("get_plants", {"active_only": True})
```

## 🔗 See Also

- [API Reference](api-reference.md) - Complete REST API documentation
- [Security Model](security.md) - Authentication and authorization
- [Configuration](configuration.md) - Server configuration options
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

---

For more information about Model Context Protocol, visit the [official MCP documentation](https://modelcontextprotocol.io/).