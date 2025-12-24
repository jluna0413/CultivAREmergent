import subprocess
import os
import sys
import time
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("a:/dev/CultivAREmergant")
ML_DIR = PROJECT_ROOT / "ml"
TOOLS_DIR = ML_DIR / "tools"
FINE_TUNING_DIR = ML_DIR / "fine_tuning"
DEPLOYMENT_DIR = ML_DIR / "deployment"
MODEL_OUTPUT_DIR = ML_DIR / "models" / "functiongemma_lora"

def run_step(description, command, shell=False):
    """Run a pipeline step with logging."""
    print(f"\n🚀 [STEP] {description}...")
    start_time = time.time()
    
    try:
        if shell:
            subprocess.run(command, shell=True, check=True, cwd=PROJECT_ROOT)
        else:
            subprocess.run(command, check=True, cwd=PROJECT_ROOT)
            
        duration = time.time() - start_time
        print(f"✅ [SUCCESS] Completed in {duration:.1f}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ [ERROR] Step failed: {e}")
        return False

def main():
    print("🌿 CultivAR Plant Health - Local Training & Deployment Pipeline")
    print("=============================================================")
    
    # 1. Dataset Preparation
    if not run_step(
        "Preparing Function Calling Dataset",
        [sys.executable, str(TOOLS_DIR / "prepare_function_dataset.py")]
    ):
        return

    # 2. Local Fine-Tuning (Unsloth)
    print("\n⚠️  Note: Training requires CUDA GPU. If this fails, install unsloth.")
    if not run_step(
        "Running Local Fine-Tuning (Unsloth)",
        [sys.executable, str(FINE_TUNING_DIR / "local_train_unsloth.py")]
    ):
        return

    # 3. Model Conversion & Deployment
    # Ensure script is executable (on Linux/Mac, but good practice)
    # convert_script = DEPLOYMENT_DIR / "convert_function_model.sh"
    # subprocess.run(["chmod", "+x", str(convert_script)], check=False)
    
    # We pass the model output directory to the conversion script
    # Note: On Windows with Git Bash/WSL, .sh scripts might need specific handling.
    # We'll stick to python subprocess calling bash if available, or assume standard shell.
    # For Windows standard command prompt, .sh execution might require 'bash' command.
    
    deploy_cmd = f'bash "{DEPLOYMENT_DIR}/convert_function_model.sh" "{MODEL_OUTPUT_DIR}"'
    
    if not run_step(
        "Converting & Deploying to Ollama",
        deploy_cmd,
        shell=True 
    ):
        return

    print("\n✨ Pipeline Completed Successfully!")
    print("🤖 Model is ready in Ollama: 'cultivar-function-gemma:latest'")
    print("👉 Test it: ollama run cultivar-function-gemma:latest")

if __name__ == "__main__":
    main()
