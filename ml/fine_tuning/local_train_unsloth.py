from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os

# Configuration
MODEL_NAME = "google/functiongemma-2b-it"
DATASET_PATH = "ml/datasets/function_calling/train_data.jsonl"
OUTPUT_DIR = "ml/models/functiongemma_lora"
MAX_SEQ_LENGTH = 2048
LORA_RANK = 16

def train():
    """Run local fine-tuning using Unsloth."""
    
    # 1. Load Model and Tokenizer
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_NAME,
        max_seq_length = MAX_SEQ_LENGTH,
        load_in_4bit = True,
        device_map = "auto",
    )

    # 2. Add LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r = LORA_RANK,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                         "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
        use_rslora = False,
        loftq_config = None,
    )

    # 3. Load Dataset
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset not found at {DATASET_PATH}. Run prepare_function_dataset.py first.")
        return

    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

    # 4. Set up Trainer
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = MAX_SEQ_LENGTH,
        dataset_num_proc = 2,
        packing = False, # Can be True for faster training
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60, # Small number for demonstration/local test
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
        ),
    )

    # 5. Train
    print("🚀 Starting training...")
    trainer_stats = trainer.train()
    print(f"✅ Training complete! Stats: {trainer_stats}")

    # 6. Save Model
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"📦 Model saved to {OUTPUT_DIR}")

    # 7. (Optional) Export to GGUF for local/mobile
    # model.save_pretrained_gguf(OUTPUT_DIR + "_gguf", tokenizer, quantization_method = "q4_k_m")

if __name__ == "__main__":
    try:
        train()
    except Exception as e:
        print(f"❌ Error during training: {e}")
        print("\nEnsure you have unsloth installed: pip install unsloth")
