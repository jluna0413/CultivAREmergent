"""
Model Loader for Fine-Tuned Plant Health Vision

Handles loading of fine-tuned Qwen3-VL model with multiple backend options:
1. Local LoRA adapters + base model (HuggingFace)
2. Ollama (GGUF format)
3. Cloud API (Modal/Replicate)

Automatically falls back to mock responses if model unavailable.
"""

import os
import logging
from typing import Optional, Dict, Any, Literal
from pathlib import Path

# Optional ML dependencies
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

logger = logging.getLogger(__name__)

ModelBackend = Literal["transformers", "ollama", "api", "mock"]


class PlantHealthModelLoader:
    """
    Intelligent model loader with automatic fallback.
    
    Load order:
    1. Local LoRA adapters (if available)
    2. Ollama (if running)
    3. Cloud API (if configured)
    4. Mock responses (fallback)
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        backend: Optional[ModelBackend] = None,
        device: str = "auto",
    ):
        self.model_path = model_path or self._get_default_model_path()
        self.backend = backend or self._detect_backend()
        self.device = device
        self.model = None
        self.processor = None
        
        logger.info(f"Initializing PlantHealthModelLoader with backend: {self.backend}")
        
    def load(self):
        """Load the model based on selected backend."""
        if self.backend == "transformers":
            self._load_transformers()
        elif self.backend == "ollama":
            self._load_ollama()
        elif self.backend == "api":
            self._load_api()
        else:
            self._load_mock()
            
    def _load_transformers(self):
        """Load model using HuggingFace Transformers."""
        try:
            from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
            from peft import PeftModel
            
            logger.info(f"Loading base model Qwen2-VL-2B-Instruct...")
            
            # Load base model
            base_model = Qwen2VLForConditionalGeneration.from_pretrained(
                "Qwen/Qwen2-VL-2B-Instruct",
                device_map=self.device,
                torch_dtype=torch.float16 if HAS_TORCH else None,
                trust_remote_code=True,
            )
            
            # Load LoRA adapters if available
            if os.path.exists(self.model_path):
                logger.info(f"Loading LoRA adapters from {self.model_path}")
                self.model = PeftModel.from_pretrained(base_model, self.model_path)
            else:
                logger.warning(f"LoRA adapters not found at {self.model_path}, using base model")
                self.model = base_model
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(
                self.model_path if os.path.exists(self.model_path) else "Qwen/Qwen2-VL-2B-Instruct",
                trust_remote_code=True
            )
            
            logger.info("✅ Model loaded successfully with Transformers backend")
            
        except Exception as e:
            logger.error(f"Failed to load Transformers model: {e}")
            logger.info("Falling back to mock backend")
            self.backend = "mock"
            self._load_mock()
    
    def _load_ollama(self):
        """Load model from Ollama."""
        try:
            import requests
            
            # Test Ollama connection
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                
                # Look for our fine-tuned model
                cultivar_models = [m for m in models if "cultivar" in m["name"].lower() or "plant-health" in m["name"].lower()]
                
                if cultivar_models:
                    self.model_name = cultivar_models[0]["name"]
                    logger.info(f"✅ Using Ollama model: {self.model_name}")
                    self.model = "ollama"  # Marker that Ollama is available
                else:
                    # Fallback to any Qwen3-VL model
                    qwen_models = [m for m in models if "qwen3-vl" in m["name"].lower() or "qwen2-vl" in m["name"].lower()]
                    if qwen_models:
                        self.model_name = qwen_models[0]["name"]
                        logger.warning(f"Fine-tuned model not found, using base: {self.model_name}")
                        self.model = "ollama"
                    else:
                        raise Exception("No Qwen VL models found in Ollama")
            else:
                raise Exception("Ollama not responding")
                
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            logger.info("Falling back to mock backend")
            self.backend = "mock"
            self._load_mock()
    
    def _load_api(self):
        """Load model via cloud API."""
        # Placeholder for cloud API integration
        # Would integrate with Modal, Replicate, or custom endpoint
        logger.info("Cloud API backend not yet implemented")
        self.backend = "mock"
        self._load_mock()
    
    def _load_mock(self):
        """Fallback to mock responses."""
        logger.info("Using mock backend (no model loaded)")
        self.model = "mock"
    
    def _get_default_model_path(self) -> str:
        """Get default path for fine-tuned model."""
        # Check common locations
        possible_paths = [
            "/app/ml/models/plant_health_vision_lora",
            "./ml/models/plant_health_vision_lora",
            os.path.expanduser("~/cultivar_models/plant_health_vision_lora"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return possible_paths[0]  # Return first as default
    
    def _detect_backend(self) -> ModelBackend:
        """Auto-detect best available backend."""
        # Try Ollama first (fastest for inference)
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            if response.status_code == 200:
                logger.info("Detected Ollama - using as backend")
                return "ollama"
        except:
            pass
        
        # Try Transformers (if GPU available and torch installed)
        if HAS_TORCH:
            try:
                import transformers
                if torch.cuda.is_available():
                    logger.info("Detected CUDA GPU - using Transformers backend")
                    return "transformers"
            except:
                pass
        
        # Fallback to mock
        logger.info("No ML backend available - using mock")
        return "mock"
    
    async def analyze_image(
        self,
        image_data: str,
        question: str = "Analyze this plant for health issues. Describe any deficiencies, pests, or diseases you see.",
        max_tokens: int = 512,
    ) -> str:
        """
        Analyze plant image and return diagnosis.
        
        Args:
            image_data: Base64 encoded image
            question: Question to ask about the image
            max_tokens: Maximum response length
            
        Returns:
            Analysis text
        """
        if self.backend == "transformers":
            return await self._analyze_transformers(image_data, question, max_tokens)
        elif self.backend == "ollama":
            return await self._analyze_ollama(image_data, question, max_tokens)
        elif self.backend == "api":
            return await self._analyze_api(image_data, question, max_tokens)
        else:
            return await self._analyze_mock(image_data, question, max_tokens)
    
    async def _analyze_transformers(self, image_data: str, question: str, max_tokens: int) -> str:
        """Analyze using Transformers backend."""
        import base64
        from PIL import Image
        from io import BytesIO
        
        # Decode image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": "You are an expert plant health advisor specializing in cannabis cultivation. Provide accurate, actionable diagnoses."
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": question}
                ]
            }
        ]
        
        # Apply chat template
        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Process inputs
        inputs = self.processor(
            text=[text],
            images=[image],
            return_tensors="pt"
        ).to(self.model.device)
        
        # Generate
        if HAS_TORCH:
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True,
                )
        else:
            return await self._analyze_mock(image_data, question, max_tokens)
        
        # Decode
        response = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        response = response.split("assistant\n")[-1].strip()
        
        return response
    
    async def _analyze_ollama(self, image_data: str, question: str, max_tokens: int) -> str:
        """Analyze using Ollama backend."""
        import requests
        
        payload = {
            "model": self.model_name,
            "prompt": question,
            "images": [image_data],
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get("response", "Error: No response from model")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    async def _analyze_api(self, image_data: str, question: str, max_tokens: int) -> str:
        """Analyze using cloud API."""
        # Placeholder for cloud API
        return "Cloud API not yet implemented"
    
    async def _analyze_mock(self, image_data: str, question: str, max_tokens: int) -> str:
        """Mock analysis (fallback)."""
        return (
            "Early Nitrogen Deficiency detected. "
            "Lower leaves showing slight yellowing, starting from tips. "
            "Solution: Increase nitrogen in feeding schedule by 10-15%, "
            "check pH (optimal 6.0-6.5), consider foliar feeding for quick response. "
            "Monitor lower leaves weekly and maintain consistent feeding schedule."
        )


# Global instance (lazy loaded)
_model_loader: Optional[PlantHealthModelLoader] = None


def get_model_loader() -> PlantHealthModelLoader:
    """Get or create global model loader instance."""
    global _model_loader
    
    if _model_loader is None:
        _model_loader = PlantHealthModelLoader()
        _model_loader.load()
    
    return _model_loader
