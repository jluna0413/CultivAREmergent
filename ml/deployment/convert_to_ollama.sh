#!/bin/bash
#
# Automated Model Conversion: HuggingFace → GGUF → Ollama
# Converts fine-tuned Qwen3-VL model to GGUF format and imports to Ollama
#
# Usage: ./convert_to_ollama.sh /path/to/lora_adapters
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}CultivAR Plant Health Model Converter${NC}"
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
OUTPUT_DIR="${SCRIPT_DIR}/converted_models"
TEMP_DIR="${SCRIPT_DIR}/temp_conversion"

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
    echo "  Visit: https://ollama.ai"
    exit 1
fi
echo "  ✓ Ollama found"

# Check if llama.cpp is available
if [ ! -d "${SCRIPT_DIR}/llama.cpp" ]; then
    echo -e "${YELLOW}  llama.cpp not found, cloning...${NC}"
    git clone https://github.com/ggerganov/llama.cpp.git "${SCRIPT_DIR}/llama.cpp"
    cd "${SCRIPT_DIR}/llama.cpp"
    make
    cd "$SCRIPT_DIR"
fi
echo "  ✓ llama.cpp ready"

echo -e "\n${YELLOW}[2/5] Merging LoRA adapters with base model...${NC}"

python3 << EOF
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from peft import PeftModel
import os

print("Loading base model...")
base_model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
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

# Save processor
processor = AutoProcessor.from_pretrained("${LORA_PATH}", trust_remote_code=True)
processor.save_pretrained("${TEMP_DIR}/merged_model")

print("✓ Model merged successfully")
EOF

echo -e "${GREEN}  ✓ LoRA merged with base model${NC}"

echo -e "\n${YELLOW}[3/5] Converting to GGUF format...${NC}"

# Convert to GGUF using llama.cpp
python "${SCRIPT_DIR}/llama.cpp/convert_hf_to_gguf.py" \
    "${TEMP_DIR}/merged_model" \
    --outfile "${OUTPUT_DIR}/cultivar_plant_health_vision_f16.gguf" \
    --outtype f16

echo -e "${GREEN}  ✓ Converted to F16 GGUF${NC}"

echo -e "\n${YELLOW}[4/5] Quantizing to Q4_K_M (4-bit, optimal for Ollama)...${NC}"

"${SCRIPT_DIR}/llama.cpp/llama-quantize" \
    "${OUTPUT_DIR}/cultivar_plant_health_vision_f16.gguf" \
    "${OUTPUT_DIR}/cultivar_plant_health_vision_q4_k_m.gguf" \
    Q4_K_M

echo -e "${GREEN}  ✓ Quantized to Q4_K_M${NC}"

echo -e "\n${YELLOW}[5/5] Importing to Ollama...${NC}"

# Create Modelfile
cat > "${TEMP_DIR}/Modelfile" << 'MODELFILE'
FROM ./cultivar_plant_health_vision_q4_k_m.gguf

TEMPLATE """{{- if .System }}
<|im_start|>system
{{ .System }}<|im_end|>
{{- end }}
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

SYSTEM """You are an expert plant health advisor specializing in cannabis cultivation. You provide accurate, actionable advice for diagnosing and treating plant health issues including nutrient deficiencies, pests, diseases, and environmental stress."""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
MODELFILE

# Import to Ollama
cd "$OUTPUT_DIR"
ollama create cultivar-plant-health:latest -f "${TEMP_DIR}/Modelfile"

echo -e "${GREEN}  ✓ Model imported to Ollama${NC}"

echo -e "\n${YELLOW}Testing model...${NC}"

# Test the model
ollama run cultivar-plant-health:latest "What are signs of nitrogen deficiency?" --verbose=false | head -n 5

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}Conversion Complete!${NC}"
echo -e "${GREEN}=========================================${NC}\n"

echo -e "Model available as: ${GREEN}cultivar-plant-health:latest${NC}"
echo -e "\nTest it with:"
echo -e "  ${YELLOW}ollama run cultivar-plant-health:latest \"Diagnose plant health issues\"${NC}\n"

echo -e "Files created:"
echo -e "  - ${OUTPUT_DIR}/cultivar_plant_health_vision_f16.gguf (FP16)"
echo -e "  - ${OUTPUT_DIR}/cultivar_plant_health_vision_q4_k_m.gguf (Q4_K_M - recommended)"

echo -e "\n${YELLOW}Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"

echo -e "${GREEN}Done!${NC}\n"
