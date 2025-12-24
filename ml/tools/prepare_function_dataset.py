import json
import os
import random
from typing import List, Dict, Any

# Template for FunctionGemma Chat Format
# Reference: https://docs.unsloth.ai/models/functiongemma

SYSTEM_PROMPT = "You are a model that can do function calling with the following functions"

TOOLS = [
    {
        "name": "analyze_plant_health",
        "description": "Analyze plant photo for health issues using AI vision",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "image_data": {"type": "STRING", "description": "Base64 encoded plant photo"},
                "plant_id": {"type": "INTEGER", "description": "ID of the plant"},
                "growth_stage": {"type": "STRING", "enum": ["seedling", "vegetative", "flowering", "harvest"]}
            },
            "required": ["image_data"]
        }
    },
    {
        "name": "award_xp",
        "description": "Award XP to a user for positive actions",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "user_id": {"type": "INTEGER"},
                "amount": {"type": "INTEGER"},
                "source": {"type": "STRING", "description": "Reason for awarding XP"}
            },
            "required": ["user_id", "amount", "source"]
        }
    },
    {
        "name": "optimize_environment",
        "description": "Adjust environment setpoints (VPD, Temp, Humidity)",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "temp_target": {"type": "NUMBER"},
                "humidity_target": {"type": "NUMBER"},
                "vpd_target": {"type": "NUMBER"}
            }
        }
    }
]

def format_tool_declaration(tool: Dict[str, Any]) -> str:
    """Format a tool into the FunctionGemma declaration block."""
    params = json.dumps(tool["parameters"]).replace('"', '<escape>').replace(' ', '')
    return f"<start_function_declaration>declaration:{tool['name']}{{description:<escape>{tool['description']}<escape>,parameters:{params}}}<end_function_declaration>"

def build_prompt(user_query: str) -> str:
    """Build the full FunctionGemma prompt with tool declarations."""
    declarations = "".join([format_tool_declaration(t) for t in TOOLS])
    return f"<bos><start_of_turn>developer\n{SYSTEM_PROMPT}{declarations}<end_of_turn>\n<start_of_turn>user\n{user_query}<end_of_turn>\n<start_of_turn>model\n"

def generate_examples():
    """Generate synthetic examples for training."""
    examples = []
    
    # Example 1: Plant Health
    examples.append({
        "user": "I just took a photo of my seedling. It looks a bit yellow. Can you check it? ID is 42.",
        "think": "The user wants to analyze a plant photo. I should use the analyze_plant_health tool. They provided plant_id 42 and growth_stage seedling.",
        "call": "call:analyze_plant_health{image_data:\"IMAGE_DATA_PLACEHOLDER\",plant_id:42,growth_stage:\"seedling\"}"
    })
    
    # Example 2: XP Awarding
    examples.append({
        "user": "User 10 has completed their daily check-in. Award them 50 XP.",
        "think": "User 10 completed a task. I need to award XP. source should be 'daily_checkin'.",
        "call": "call:award_xp{user_id:10,amount:50,source:\"daily_checkin\"}"
    })
    
    # Example 3: Environment Optimization
    examples.append({
        "user": "The tent is too humid. Set humidity to 50% and decrease temp to 24C.",
        "think": "Low humidity and temp adjustments requested. Calling optimize_environment.",
        "call": "call:optimize_environment{temp_target:24,humidity_target:50}"
    })
    
    return examples

def save_dataset(output_path: str):
    """Save the dataset in JSONL format for Unsloth training."""
    examples = generate_examples()
    with open(output_path, 'w') as f:
        for ex in examples:
            prompt = build_prompt(ex["user"])
            response = f"<think>\n{ex['think']}\n</think>\n<start_function_call>{ex['call']}<end_function_call>"
            full_text = prompt + response + "<end_of_turn>"
            f.write(json.dumps({"text": full_text}) + "\n")

if __name__ == "__main__":
    os.makedirs("ml/datasets/function_calling", exist_ok=True)
    save_dataset("ml/datasets/function_calling/train_data.jsonl")
    print(f"✅ Generated dataset at ml/datasets/function_calling/train_data.jsonl")
