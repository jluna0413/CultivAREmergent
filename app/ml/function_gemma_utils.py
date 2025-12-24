import re
import json
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FunctionGemmaParser:
    """
    Parser for FunctionGemma structured outputs.
    Handles <think> blocks and <start_function_call> blocks.
    
    Format ref: https://docs.unsloth.ai/models/functiongemma
    """
    
    @staticmethod
    def parse_response(response_text: str) -> Dict[str, Any]:
        """
        Parse the full response from FunctionGemma.
        
        Returns:
            Dict containing:
            - 'reasoning': str (content of <think>)
            - 'function_calls': List[Dict] (parsed function calls)
            - 'content': str (any other text)
        """
        result = {
            "reasoning": None,
            "function_calls": [],
            "content": ""
        }
        
        # Extract <think> content
        think_match = re.search(r"<think>(.*?)</think>", response_text, re.DOTALL)
        if think_match:
            result["reasoning"] = think_match.group(1).strip()
            # Remove think block to process rest
            remaining_text = response_text.replace(think_match.group(0), "")
        else:
            remaining_text = response_text
            
        # Extract function calls using the specific FunctionGemma format
        # Format: <start_function_call>call:func_name{args}<end_function_call>
        # Note: Args are not strict JSON, keys are unquoted. We need to be careful.
        
        # Regex to find full function call blocks
        call_pattern = r"<start_function_call>(.*?)<end_function_call>"
        calls = re.findall(call_pattern, remaining_text, re.DOTALL)
        
        for call_str in calls:
            # call_str like: call:analyze_plant_health{image_data:"...",...}
            parsed_call = FunctionGemmaParser._parse_single_call(call_str)
            if parsed_call:
                result["function_calls"].append(parsed_call)
                
        # Clean plain text content (remove tags)
        clean_text = re.sub(call_pattern, "", remaining_text).strip()
        result["content"] = clean_text
        
        return result
    
    @staticmethod
    def _parse_single_call(call_str: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single function call string.
        Example: call:award_xp{user_id:10,amount:50}
        """
        try:
            if not call_str.startswith("call:"):
                return None
                
            # Split name and args
            name_end = call_str.find("{")
            if name_end == -1:
                return None
                
            func_name = call_str[5:name_end].strip()
            args_str = call_str[name_end:] # starts with {
            
            # Simple attempt to parse args as JSON-ish
            # FunctionGemma output keys are often unquoted (e.g. user_id:10)
            # We need to quote keys to make it valid JSON
            
            # 1. Quote keys: {key: -> {"key":
            json_str = re.sub(r'(\w+):', r'"\1":', args_str)
            
            # 2. Fix potential quoting issues if values contained colons (naive fix)
            # A more robust parser might be needed for complex strings
            
            try:
                args = json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON args for {func_name}: {json_str}")
                return None
                
            return {
                "name": func_name,
                "arguments": args
            }
            
        except Exception as e:
            logger.error(f"Error parsing function call '{call_str}': {e}")
            return None
