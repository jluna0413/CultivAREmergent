# AI Assistant Setup

Configure AI assistants to work with CultivAR using the Model Context Protocol (MCP) for intelligent grow journal management.

## Supported AI Assistants

### ✅ Fully Supported
- **Claude Desktop** - Native MCP support
- **Custom MCP Clients** - Using Python/JavaScript libraries

### 🚧 In Development
- **ChatGPT Desktop** - Planned MCP support
- **LM Studio** - Community integration
- **Ollama** - Local model support

## Claude Desktop Setup

### Prerequisites
- Claude Desktop app installed
- CultivAR MCP server running
- Network connectivity between Claude and CultivAR

### Step 1: Install Claude Desktop

Download and install Claude Desktop from [claude.ai](https://claude.ai/download).

### Step 2: Configure MCP Connection

1. **Locate Claude Desktop config file:**

   **macOS:**
   ```bash
   ~/.config/claude-desktop/config.json
   ```

   **Windows:**
   ```bash
   %APPDATA%\claude-desktop\config.json
   ```

   **Linux:**
   ```bash
   ~/.config/claude-desktop/config.json
   ```

2. **Add CultivAR MCP server configuration:**

   ```json
   {
     "mcpServers": {
       "cultivar-grow-journal": {
         "command": "python",
         "args": [
           "/path/to/CultivAREmergent/mcp_server.py"
         ],
         "env": {
           "CULTIVAR_API_URL": "http://localhost:5000",
           "CULTIVAR_MCP_LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

3. **Update the path** to match your CultivAR installation directory.

### Step 3: Start CultivAR with MCP

```bash
cd /path/to/CultivAREmergent

# Enable MCP support
export CULTIVAR_MCP_ENABLED=true
export CULTIVAR_MCP_PORT=8001

# Start CultivAR
python cultivar_app.py --enable-mcp
```

### Step 4: Restart Claude Desktop

Close and restart Claude Desktop to load the new MCP configuration.

### Step 5: Test the Connection

In Claude Desktop, try these example prompts:

```
What plants do I have in my grow journal?
```

```
Show me the details for my Blue Dream plant
```

```
What are the current environmental conditions in my grow room?
```

## Custom AI Assistant Integration

### Python Client Example

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def interact_with_cultivar():
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/CultivAREmergent/mcp_server.py"],
        env={"CULTIVAR_API_URL": "http://localhost:5000"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Get plants
            result = await session.call_tool("get_plants", {"active_only": True})
            print("Plants:", result.content[0].text)

# Run the client
asyncio.run(interact_with_cultivar())
```

### JavaScript/Node.js Client Example

```javascript
const { StdioClientTransport, Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { spawn } = require('child_process');

async function connectToCultivAR() {
    const serverProcess = spawn('python', ['/path/to/CultivAREmergent/mcp_server.py'], {
        env: { ...process.env, CULTIVAR_API_URL: 'http://localhost:5000' }
    });
    
    const transport = new StdioClientTransport({
        stdin: serverProcess.stdin,
        stdout: serverProcess.stdout
    });
    
    const client = new Client(
        { name: "cultivar-client", version: "1.0.0" },
        { capabilities: {} }
    );
    
    await client.connect(transport);
    
    // List available tools
    const tools = await client.listTools();
    console.log('Available tools:', tools.tools.map(t => t.name));
    
    // Get plants
    const result = await client.callTool({
        name: "get_plants",
        arguments: { active_only: true }
    });
    console.log('Plants:', result.content[0].text);
}

connectToCultivAR().catch(console.error);
```

## Advanced Configuration

### Authentication Setup

For production environments, enable authentication:

```bash
# Generate API key
export CULTIVAR_MCP_API_KEY="your-secure-api-key-here"
export CULTIVAR_MCP_AUTH_REQUIRED=true

# Update Claude Desktop config
```

```json
{
  "mcpServers": {
    "cultivar-grow-journal": {
      "command": "python",
      "args": ["/path/to/CultivAREmergent/mcp_server.py"],
      "env": {
        "CULTIVAR_API_URL": "http://localhost:5000",
        "CULTIVAR_MCP_API_KEY": "your-secure-api-key-here"
      }
    }
  }
}
```

### Remote Server Setup

For remote CultivAR servers:

```json
{
  "mcpServers": {
    "cultivar-grow-journal": {
      "command": "python",
      "args": ["/path/to/CultivAREmergent/mcp_client.py"],
      "env": {
        "CULTIVAR_SERVER_URL": "https://your-cultivar-server.com",
        "CULTIVAR_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Custom Tool Configuration

Disable specific tools by modifying `config/mcp_config.json`:

```json
{
  "tools": {
    "plant_management": {
      "enabled": true,
      "read_only": true
    },
    "environmental_data": {
      "enabled": true,
      "historical_limit": "7d"
    },
    "reporting": {
      "enabled": false
    }
  }
}
```

## Usage Examples

### Basic Plant Management

**Query all active plants:**
```
AI: "Show me all my active plants and their current status"
```

**Get plant details:**
```
AI: "Give me detailed information about my Blue Dream plant"
```

**Record plant activity:**
```
AI: "Record that I watered plant #1 with 500ml of water today"
```

### Environmental Monitoring

**Check current conditions:**
```
AI: "What are the current temperature and humidity levels in my grow room?"
```

**Historical data analysis:**
```
AI: "Show me the temperature trends for the past week"
```

### Strain Information

**Search strains:**
```
AI: "Show me all indica-dominant strains in my database"
```

**Strain recommendations:**
```
AI: "What strains would be good for a beginner grower?"
```

## Troubleshooting

### Common Issues

**"MCP server not found" error:**
```bash
# Check if MCP server is executable
python /path/to/CultivAREmergent/mcp_server.py
```

**Connection refused:**
```bash
# Verify CultivAR is running
curl http://localhost:5000

# Check MCP configuration
export CULTIVAR_MCP_LOG_LEVEL=DEBUG
```

**Tool not working:**
```bash
# Test individual tools
python -c "
import asyncio
from mcp_server import CultivARData
print(CultivARData.get_plants())
"
```

### Debug Mode

Enable detailed logging:

```bash
export CULTIVAR_MCP_LOG_LEVEL=DEBUG
export CULTIVAR_DEBUG=true
```

Check logs:
```bash
tail -f logs/mcp_server.log
```

### Validation Commands

**Test MCP server directly:**
```bash
python mcp_server.py
# Should start without errors
```

**Test with curl:**
```bash
curl -X POST http://localhost:8001/mcp/tools/get_plants \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"active_only": true}}'
```

## Best Practices

### Security
- ✅ Use API keys for authentication
- ✅ Enable HTTPS for remote connections
- ✅ Regularly rotate API keys
- ✅ Monitor MCP access logs

### Performance
- ✅ Limit historical data queries
- ✅ Use rate limiting
- ✅ Cache frequent queries
- ✅ Monitor resource usage

### Usage
- ✅ Use specific, clear prompts
- ✅ Verify data before making changes
- ✅ Keep MCP server updated
- ✅ Regular backup of grow data

## 🔗 See Also

- [MCP Integration](mcp-integration.md) - Complete MCP documentation
- [API Reference](api-reference.md) - REST API endpoints
- [Configuration](configuration.md) - Server configuration options
- [Security Model](security.md) - Authentication and authorization

---

*For more AI assistant integrations, check our [community examples](https://github.com/jluna0413/CultivAREmergent/wiki/AI-Integrations)*