"""
CultivAR MCP (Model Context Protocol) Server

This module implements the MCP server for CultivAR, enabling AI assistants and LLMs
to interact with grow journal data in a structured, secure way.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ReadResourceRequest,
    ReadResourceResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cultivar-mcp")

# Mock data for demonstration - in real implementation, this would connect to the database
class CultivARData:
    """Mock data access layer for CultivAR database"""
    
    @staticmethod
    def get_plants(active_only: bool = False, strain_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get plants from the database"""
        plants = [
            {
                "id": 1,
                "name": "Blue Dream #1",
                "strain_id": 1,
                "strain": "Blue Dream",
                "stage": "flowering",
                "days_in_stage": 42,
                "last_activity": "2024-01-15T10:30:00Z",
                "status": "active"
            },
            {
                "id": 2,
                "name": "Purple Haze #2",
                "strain_id": 2,
                "strain": "Purple Haze",
                "stage": "vegetative",
                "days_in_stage": 28,
                "last_activity": "2024-01-14T16:45:00Z",
                "status": "active"
            },
            {
                "id": 3,
                "name": "White Widow #3",
                "strain_id": 3,
                "strain": "White Widow",
                "stage": "harvested",
                "days_in_stage": 0,
                "last_activity": "2024-01-10T14:20:00Z",
                "status": "harvested"
            }
        ]
        
        if active_only:
            plants = [p for p in plants if p["status"] == "active"]
        
        if strain_id:
            plants = [p for p in plants if p["strain_id"] == strain_id]
            
        return plants
    
    @staticmethod
    def get_plant_details(plant_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific plant"""
        plants = CultivARData.get_plants()
        plant = next((p for p in plants if p["id"] == plant_id), None)
        
        if plant:
            # Add more detailed information
            plant.update({
                "description": f"Detailed information for {plant['name']}",
                "planted_date": "2023-12-01T00:00:00Z",
                "expected_harvest": "2024-02-15T00:00:00Z",
                "current_height": 85.5,
                "current_width": 45.2,
                "ph_level": 6.2,
                "ec_level": 1.8,
                "notes": "Growing well, good color and structure"
            })
        
        return plant
    
    @staticmethod
    def get_strains(search: Optional[str] = None, genetics: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get strain information"""
        strains = [
            {
                "id": 1,
                "name": "Blue Dream",
                "genetics": "hybrid",
                "indica_percentage": 40,
                "sativa_percentage": 60,
                "breeder": "DJ Short",
                "flowering_time": "9-10 weeks",
                "description": "Popular hybrid with balanced effects"
            },
            {
                "id": 2,
                "name": "Purple Haze",
                "genetics": "sativa",
                "indica_percentage": 20,
                "sativa_percentage": 80,
                "breeder": "Jimi Hendrix Seeds",
                "flowering_time": "10-12 weeks",
                "description": "Classic sativa with uplifting effects"
            },
            {
                "id": 3,
                "name": "White Widow",
                "genetics": "hybrid",
                "indica_percentage": 60,
                "sativa_percentage": 40,
                "breeder": "Green House Seeds",
                "flowering_time": "8-9 weeks",
                "description": "Famous hybrid with high resin production"
            }
        ]
        
        if search:
            strains = [s for s in strains if search.lower() in s["name"].lower()]
        
        if genetics:
            strains = [s for s in strains if s["genetics"] == genetics.lower()]
            
        return strains
    
    @staticmethod
    def get_environmental_data(start_date: Optional[str] = None, end_date: Optional[str] = None, sensor_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get environmental sensor data"""
        data = [
            {
                "timestamp": "2024-01-15T12:00:00Z",
                "temperature": 24.5,
                "humidity": 55.2,
                "light_level": 850,
                "co2_level": 1200,
                "sensor_type": "climate"
            },
            {
                "timestamp": "2024-01-15T18:00:00Z",
                "temperature": 22.1,
                "humidity": 58.7,
                "light_level": 0,
                "co2_level": 800,
                "sensor_type": "climate"
            }
        ]
        
        if sensor_type:
            data = [d for d in data if d["sensor_type"] == sensor_type]
            
        return data
    
    @staticmethod
    def add_plant_activity(plant_id: int, activity_type: str, notes: Optional[str] = None, amount: Optional[float] = None) -> Dict[str, Any]:
        """Add a new activity for a plant"""
        activity = {
            "id": 123,  # Mock ID
            "plant_id": plant_id,
            "activity_type": activity_type,
            "notes": notes,
            "amount": amount,
            "timestamp": datetime.now().isoformat() + "Z",
            "success": True
        }
        return activity


# Initialize the MCP server
server = Server("cultivar-mcp")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available MCP tools for CultivAR"""
    return [
        Tool(
            name="get_plants",
            description="Retrieve all plants in the grow journal",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "description": "Only return active plants"
                    },
                    "strain_id": {
                        "type": "integer",
                        "description": "Filter by strain ID"
                    }
                }
            }
        ),
        Tool(
            name="get_plant_details",
            description="Get detailed information about a specific plant",
            inputSchema={
                "type": "object",
                "properties": {
                    "plant_id": {
                        "type": "integer",
                        "description": "Plant ID to retrieve",
                        "required": True
                    }
                },
                "required": ["plant_id"]
            }
        ),
        Tool(
            name="get_strains",
            description="Retrieve strain database information",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search term for strain names"
                    },
                    "genetics": {
                        "type": "string",
                        "description": "Filter by genetic type",
                        "enum": ["indica", "sativa", "hybrid"]
                    }
                }
            }
        ),
        Tool(
            name="get_environmental_data",
            description="Retrieve sensor data and environmental conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date (ISO format)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (ISO format)"
                    },
                    "sensor_type": {
                        "type": "string",
                        "description": "Filter by sensor type"
                    }
                }
            }
        ),
        Tool(
            name="add_plant_activity",
            description="Record a new activity for a plant",
            inputSchema={
                "type": "object",
                "properties": {
                    "plant_id": {
                        "type": "integer",
                        "description": "Target plant ID",
                        "required": True
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "Type of activity (watering, feeding, etc.)",
                        "required": True
                    },
                    "notes": {
                        "type": "string",
                        "description": "Activity notes"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount for measurements"
                    }
                },
                "required": ["plant_id", "activity_type"]
            }
        ),
        Tool(
            name="get_grow_room_status",
            description="Get current environmental conditions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from the MCP client"""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    try:
        if name == "get_plants":
            active_only = arguments.get("active_only", False)
            strain_id = arguments.get("strain_id")
            plants = CultivARData.get_plants(active_only=active_only, strain_id=strain_id)
            
            return [TextContent(
                type="text",
                text=f"Found {len(plants)} plants:\n\n" + 
                     "\n".join([
                         f"• {plant['name']} (ID: {plant['id']})\n"
                         f"  Strain: {plant['strain']}\n"
                         f"  Stage: {plant['stage']} ({plant['days_in_stage']} days)\n"
                         f"  Last Activity: {plant['last_activity']}\n"
                         for plant in plants
                     ])
            )]
        
        elif name == "get_plant_details":
            plant_id = arguments.get("plant_id")
            if not plant_id:
                return [TextContent(type="text", text="Error: plant_id is required")]
            
            plant = CultivARData.get_plant_details(plant_id)
            if not plant:
                return [TextContent(type="text", text=f"Plant with ID {plant_id} not found")]
            
            return [TextContent(
                type="text",
                text=f"Plant Details: {plant['name']}\n\n"
                     f"Strain: {plant['strain']}\n"
                     f"Stage: {plant['stage']} ({plant['days_in_stage']} days)\n"
                     f"Planted: {plant['planted_date']}\n"
                     f"Expected Harvest: {plant['expected_harvest']}\n"
                     f"Current Height: {plant['current_height']} cm\n"
                     f"Current Width: {plant['current_width']} cm\n"
                     f"pH Level: {plant['ph_level']}\n"
                     f"EC Level: {plant['ec_level']}\n"
                     f"Notes: {plant['notes']}"
            )]
        
        elif name == "get_strains":
            search = arguments.get("search")
            genetics = arguments.get("genetics")
            strains = CultivARData.get_strains(search=search, genetics=genetics)
            
            return [TextContent(
                type="text",
                text=f"Found {len(strains)} strains:\n\n" +
                     "\n".join([
                         f"• {strain['name']} (ID: {strain['id']})\n"
                         f"  Genetics: {strain['genetics']} ({strain['indica_percentage']}% Indica, {strain['sativa_percentage']}% Sativa)\n"
                         f"  Breeder: {strain['breeder']}\n"
                         f"  Flowering Time: {strain['flowering_time']}\n"
                         f"  Description: {strain['description']}\n"
                         for strain in strains
                     ])
            )]
        
        elif name == "get_environmental_data":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            sensor_type = arguments.get("sensor_type")
            data = CultivARData.get_environmental_data(start_date=start_date, end_date=end_date, sensor_type=sensor_type)
            
            return [TextContent(
                type="text",
                text=f"Environmental Data ({len(data)} readings):\n\n" +
                     "\n".join([
                         f"• {reading['timestamp']}\n"
                         f"  Temperature: {reading['temperature']}°C\n"
                         f"  Humidity: {reading['humidity']}%\n"
                         f"  Light Level: {reading['light_level']} lux\n"
                         f"  CO2 Level: {reading['co2_level']} ppm\n"
                         for reading in data
                     ])
            )]
        
        elif name == "add_plant_activity":
            plant_id = arguments.get("plant_id")
            activity_type = arguments.get("activity_type")
            notes = arguments.get("notes")
            amount = arguments.get("amount")
            
            if not plant_id or not activity_type:
                return [TextContent(type="text", text="Error: plant_id and activity_type are required")]
            
            result = CultivARData.add_plant_activity(plant_id=plant_id, activity_type=activity_type, notes=notes, amount=amount)
            
            return [TextContent(
                type="text",
                text=f"Activity recorded successfully!\n\n"
                     f"Activity ID: {result['id']}\n"
                     f"Plant ID: {result['plant_id']}\n"
                     f"Activity Type: {result['activity_type']}\n"
                     f"Amount: {result['amount'] or 'N/A'}\n"
                     f"Notes: {result['notes'] or 'None'}\n"
                     f"Timestamp: {result['timestamp']}"
            )]
        
        elif name == "get_grow_room_status":
            # Get current environmental status
            current_data = CultivARData.get_environmental_data()
            if current_data:
                latest = current_data[0]  # Most recent reading
                return [TextContent(
                    type="text",
                    text=f"Current Grow Room Status:\n\n"
                         f"Temperature: {latest['temperature']}°C\n"
                         f"Humidity: {latest['humidity']}%\n"
                         f"Light Level: {latest['light_level']} lux\n"
                         f"CO2 Level: {latest['co2_level']} ppm\n"
                         f"Last Updated: {latest['timestamp']}\n\n"
                         f"Status: All systems normal ✅"
                )]
            else:
                return [TextContent(type="text", text="No environmental data available")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error handling tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="cultivar://plants",
            name="All Plants",
            description="Complete list of all plants in the grow journal",
            mimeType="application/json"
        ),
        Resource(
            uri="cultivar://strains",
            name="Strain Database",
            description="Complete strain database with genetics information",
            mimeType="application/json"
        ),
        Resource(
            uri="cultivar://environmental",
            name="Environmental Data",
            description="Current and historical environmental sensor data",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Get resource content"""
    if uri == "cultivar://plants":
        plants = CultivARData.get_plants()
        return str(plants)
    elif uri == "cultivar://strains":
        strains = CultivARData.get_strains()
        return str(strains)
    elif uri == "cultivar://environmental":
        data = CultivARData.get_environmental_data()
        return str(data)
    else:
        raise ValueError(f"Unknown resource: {uri}")

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting CultivAR MCP Server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cultivar-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())