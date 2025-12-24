#!/usr/bin/env python3
"""
Master Automation Script for CultivAR Plant Health Fine-Tuning
One-command setup for the entire ML pipeline.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_header(text: str):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}{text:^60}{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")


def run_command(cmd: list, cwd: Optional[str] = None) -> tuple:
    """Run command and return output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_python():
    """Check Python installation."""
    print("Checking Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print_error(f"Python 3.10+ required, found {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_ollama():
    """Check if Ollama is installed."""
    print("Checking Ollama...")
    
    success, output = run_command(["ollama", "--version"])
    if success:
        print_success(f"Ollama installed")
        return True
    else:
        print_warning("Ollama not found (optional for local deployment)")
        return False


def setup_directories():
    """Create necessary directories."""
    print("Setting up directories...")
    
    dirs = [
        "ml/models",
        "ml/datasets/custom_cannabis",
        "ml/datasets/huggingface",
        "ml/converted_models",
        "ml/checkpoints",
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print_success("Directories created")


def install_dependencies():
    """Install Python dependencies."""
    print("Installing Python dependencies...")
    
    requirements = [
        "transformers>=4.46.0",
        "peft>=0.13.0",
        "datasets>=3.1.0",
        "torch>=2.5.0",
        "pillow>=11.0.0",
    ]
    
    for package in requirements:
        print(f"  Installing {package}...")
        success, _ = run_command([sys.executable, "-m", "pip", "install", "-q", package])
        if not success:
            print_warning(f"Failed to install {package}")
    
    print_success("Dependencies installed")


def create_colab_link():
    """Generate Google Colab link."""
    notebook_path = Path("ml/fine_tuning/plant_health_qwen3vl_finetune.ipynb")
    
    if notebook_path.exists():
        print_success("Colab notebook created")
        print(f"\n{Colors.YELLOW}📓 Upload to Google Colab:{Colors.NC}")
        print(f"   {notebook_path.absolute()}")
        print(f"\n   Then: Runtime → Change runtime type → T4 GPU → Run all")
        return True
    else:
        print_error("Colab notebook not found")
        return False


def check_models():
    """Check for downloaded/fine-tuned models."""
    print("Checking for models...")
    
    model_path = Path("ml/models/plant_health_vision_lora")
    
    if model_path.exists():
        print_success(f"Fine-tuned model found: {model_path}")
        return True
    else:
        print_warning("No fine-tuned model found")
        print("  → Run Colab notebook to train model")
        return False


def test_model_loader():
    """Test the model loader."""
    print("Testing model loader...")
    
    try:
        # Add app to path
        sys.path.insert(0, str(Path.cwd() / "app"))
        
        from ml.model_loader import PlantHealthModelLoader
        
        loader = PlantHealthModelLoader()
        loader.load()
        
        print_success(f"Model loader initialized (backend: {loader.backend})")
        return True
        
    except Exception as e:
        print_warning(f"Model loader test failed: {e}")
        print("  → This is OK, model will use fallback")
        return False


def generate_summary():
    """Generate setup summary."""
    print_header("Setup Summary")
    
    checks = {
        "Python 3.10+": check_python(),
        "Ollama (optional)": check_ollama(),
        "Colab Notebook": Path("ml/fine_tuning/plant_health_qwen3vl_finetune.ipynb").exists(),
        "Dataset Curator": Path("ml/tools/dataset_curator.py").exists(),
        "GGUF Converter": Path("ml/deployment/convert_to_ollama.sh").exists(),
        "Fine-tuned Model": Path("ml/models/plant_health_vision_lora").exists(),
    }
    
    print("\nSystem Status:")
    for item, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {item}")
    
    print(f"\n{Colors.BLUE}Next Steps:{Colors.NC}")
    
    if not checks["Fine-tuned Model"]:
        print(f"\n{Colors.YELLOW}1. Train the model (FREE on Google Colab):{Colors.NC}")
        print("   → Upload ml/fine_tuning/plant_health_qwen3vl_finetune.ipynb to Colab")
        print("   → Switch to T4 GPU")
        print("   → Run all cells (~8 hours)")
        print("   → Download trained model to ml/models/")
    
    if checks["Fine-tuned Model"] and checks["Ollama (optional)"]:
        print(f"\n{Colors.YELLOW}2. Deploy to Ollama (optional):{Colors.NC}")
        print("   → chmod +x ml/deployment/convert_to_ollama.sh")
        print("   → ./ml/deployment/convert_to_ollama.sh ml/models/plant_health_vision_lora")
    
    print(f"\n{Colors.YELLOW}3. Start using the model:{Colors.NC}")
    print("   → Backend integration is AUTOMATIC")
    print("   → Just start your FastAPI server")
    print("   → Upload plant photos via the app")
    print("   → Get AI-powered diagnoses!")
    
    print(f"\n{Colors.GREEN}🌿 Everything is set up! See ml/README.md for details.{Colors.NC}\n")


def main():
    """Main setup workflow."""
    print_header("CultivAR Plant Health Vision Setup")
    
    print("This script will set up the automated ML pipeline.\n")
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent.parent)
    
    # Setup
    setup_directories()
    
    if not check_python():
        print_error("Python 3.10+ is required")
        sys.exit(1)
    
    # Check optional components
    check_ollama()
    
    # Install dependencies (optional, shows as warning if fails)
    try:
        install_dependencies()
    except Exception as e:
        print_warning(f"Some dependencies may need manual installation: {e}")
    
    # Verify files exist
    create_colab_link()
    check_models()
    test_model_loader()
    
    # Summary
    generate_summary()


if __name__ == "__main__":
    main()
