#!/bin/bash
#
# Automated Model Conversion: FunctionGemma (Fine-Tuned) → GGUF → Ollama
# Converts fine-tuned FunctionGemma model to GGUF format and imports to Ollama
#
# Usage: ./convert_function_model.sh /path/to/lora_adapters
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}CultivAR FunctionGemma Converter${NC}"
echo -e "${GREEN}HuggingFace → GGUF → Ollama${NC}"
echo -e "${GREEN}=========================================${NC}\n"

# Check arguments
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No model path provided${NC}"
    echo "Usage: $0 /path/to/lora_adapters"
    exit 1
fi

LORA_PATH="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/converted_function_models"
TEMP_DIR="${SCRIPT_DIR}/temp_function_conversion"
BASE_MODEL="google/functiongemma-2b-it" 

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo -e "${YELLOW}[1/5] Checking dependencies...${NC}"

# Check for Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python not found! Please install Python 3.10+${NC}"
    exit 1
fi
echo "  ✓ Python found"

# Check for Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}Ollama not found! Please install Ollama first${NC}"
    exit 1
fi
echo "  ✓ Ollama found"

# Check for llama.cpp
if [ ! -d "${SCRIPT_DIR}/llama.cpp" ]; then
    echo -e "${YELLOW}  llama.cpp not found, cloning...${NC}"
    git clone https://github.com/ggerganov/llama.cpp.git "${SCRIPT_DIR}/llama.cpp"
    cd "${SCRIPT_DIR}/llama.cpp"
    make
    cd "$SCRIPT_DIR"
fi
echo "  ✓ llama.cpp ready"

echo -e "\n${YELLOW}[2/5] Merging LoRA adapters with base FunctionGemma...${NC}"

python3 << EOF
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

print(f"Loading base model: {BASE_MODEL}")
base_model = AutoModelForCausalLM.from_pretrained(
    "${BASE_MODEL}",
    device_map="cpu",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

print("Loading LoRA adapters...")
model = PeftModel.from_pretrained(base_model, "${LORA_PATH}")

print("Merging LoRA with base model...")
merged_model = model.merge_and_unload()

print("Saving merged model...")
merged_model.save_pretrained("${TEMP_DIR}/merged_model")

# Save tokenizer
tokenizer = AutoTokenizer.from_pretrained("${LORA_PATH}", trust_remote_code=True)
tokenizer.save_pretrained("${TEMP_DIR}/merged_model")

print("✓ Model merged successfully")
EOF

echo -e "${GREEN}  ✓ LoRA merged with base model${NC}"

echo -e "\n${YELLOW}[3/5] Converting to GGUF format...${NC}"

# Convert to GGUF using llama.cpp
python "${SCRIPT_DIR}/llama.cpp/convert_hf_to_gguf.py" \
    "${TEMP_DIR}/merged_model" \
    --outfile "${OUTPUT_DIR}/cultivar_function_gemma_f16.gguf" \
    --outtype f16

echo -e "${GREEN}  ✓ Converted to F16 GGUF${NC}"

echo -e "\n${YELLOW}[4/5] Quantizing to Q4_K_M (4-bit, mobile optimized)...${NC}"

"${SCRIPT_DIR}/llama.cpp/llama-quantize" \
    "${OUTPUT_DIR}/cultivar_function_gemma_f16.gguf" \
    "${OUTPUT_DIR}/cultivar_function_gemma_q4_k_m.gguf" \
    Q4_K_M

echo -e "${GREEN}  ✓ Quantized to Q4_K_M${NC}"

echo -e "\n${YELLOW}[5/5] Importing to Ollama...${NC}"

# Create Modelfile for FunctionGemma
# Based on Gemma2 template but ensuring tool availability isn't hardcoded in system unless needed
cat > "${TEMP_DIR}/Modelfile" << 'MODELFILE'
FROM ./cultivar_function_gemma_q4_k_m.gguf

# Gemma 2 Template
TEMPLATE """<start_of_turn>user
{{ .Prompt }}<end_of_turn>
<start_of_turn>model
{{ .Response }}<end_of_turn>
"""

# System Message (Standard FunctionGemma preamble is usually passed in user prompt or system)
SYSTEM """You are a helpful AI assistant capable of calling functions. 
Always think before you act. Output your reasoning in <think> tags.
"""

PARAMETER temperature 0.0
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.0
PARAMETER stop "<start_of_turn>"
PARAMETER stop "<end_of_turn>"
MODELFILE

# Import to Ollama
cd "$OUTPUT_DIR"
ollama create cultivar-function-gemma:latest -f "${TEMP_DIR}/Modelfile"

echo -e "${GREEN}  ✓ Model imported to Ollama${NC}"

echo -e "\n${YELLOW}Testing model...${NC}"

# Test the model
ollama run cultivar-function-gemma:latest "Hello, who are you?" --verbose=false | head -n 5

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}FunctionGemma Conversion Complete!${NC}"
echo -e "${GREEN}=========================================${NC}\n"

echo -e "Model available as: ${GREEN}cultivar-function-gemma:latest${NC}"
echo -e "Files created:"
echo -e "  - ${OUTPUT_DIR}/cultivar_function_gemma_q4_k_m.gguf (Q4_K_M)"

echo -e "\n${YELLOW}Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"

echo -e "${GREEN}Done!${NC}\n"
