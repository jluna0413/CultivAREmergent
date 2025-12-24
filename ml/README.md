# 🌿 CultivAR Plant Health Vision - Automated Setup Guide

This directory contains everything you need to fine-tune and deploy the plant health vision model.

## 📁 Directory Structure

```
ml/
├── fine_tuning/
│   └── plant_health_qwen3vl_finetune.ipynb  # Google Colab notebook
├── deployment/
│   └── convert_to_ollama.sh                  # GGUF conversion script
├── tools/
│   └── dataset_curator.py                    # Dataset curation tool
├── models/                                    # Downloaded/fine-tuned models
└── datasets/                                  # Training datasets
```

## 🚀 Complete Automation Workflow

### Phase 1: Fine-Tuning (Google Colab)

**Time: ~8 hours | Cost: FREE**

1. **Open the notebook:**
   - Upload `plant_health_qwen3vl_finetune.ipynb` to Google Colab
   - Or use this link: [[Upload to Colab]](https://colab.research.google.com)

2. **Configure runtime:**
   - Runtime → Change runtime type → **T4 GPU**
   - Save

3. **Run all cells:**
   - Runtime → Run all
   - The notebook will:
     - ✅ Install dependencies
     - ✅ Mount Google Drive
     - ✅ Download datasets
     - ✅ Fine-tune Qwen3-VL-2B with QLoRA
     - ✅ Save LoRA adapters to Drive

4. **Download the model:**
   - After ~8 hours, download `cultivar_plant_health_model.zip` from Google Drive
   - Extract to `ml/models/plant_health_vision_lora/`

### Phase 2: Local Deployment (Your Machine)

#### Option A: Use with Transformers (Requires GPU)

```bash
# Install dependencies
pip install transformers peft torch pillow

# The model loader will automatically detect and use the fine-tuned model
# No additional steps needed!
```

#### Option B: Convert to Ollama (Recommended)

```bash
# Make script executable
chmod +x ml/deployment/convert_to_ollama.sh

# Run conversion (takes ~30 minutes)
./ml/deployment/convert_to_ollama.sh ml/models/plant_health_vision_lora

# Model will be imported as: cultivar-plant-health:latest
```

Test it:
```bash
ollama run cultivar-plant-health:latest "What are signs of nitrogen deficiency?"
```

### Phase 3: Backend Integration (Automatic)

The backend integration is **already complete**! 🎉

The `PlantHealthVisionAgent` will automatically:
1. Detect available backend (Ollama → Transformers → Mock)
2. Load the fine-tuned model
3. Use it for plant health analysis
4. Fall back to mock responses if model unavailable

**No configuration needed** - it just works!

### Phase 4: Custom Data Curation (Optional)

Build your own cannabis-specific dataset:

```bash
# Interactive mode
python ml/tools/dataset_curator.py --interactive

# View statistics
python ml/tools/dataset_curator.py --stats

# Export for training
python ml/tools/dataset_curator.py --export
```

The curator will:
- Organize images
- Create structured training data
- Export in format ready for fine-tuning

Retrain with your custom data:
1. Upload new dataset to Google Colab
2. Modify notebook to use custom dataset
3. Run training again
4. Deploy updated model

## 🎯 Testing the Integration

### Test via API

```bash
curl -X POST http://localhost:4200/api/v1/ai/analyze-plant \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "plant_id": 1,
    "image_data": "base64_encoded_image_here",
    "growth_stage": "vegetative"
  }'
```

### Test via Flutter App

1. Navigate to Plant Health Analysis screen
2. Upload/capture plant photo
3. Submit for analysis
4. View AI-powered diagnosis!

## 📊 Model Performance

### Expected Results

- **Accuracy**: >85% on plant disease identification
- **Response Time**: <3 seconds
- **Confidence**: 0.7-0.9 for clear issues

### Improvement Loop

1. Collect user feedback on diagnoses
2. Add confirmed examples to custom dataset
3. Retrain monthly with new data
4. Deploy updated model
5. Repeat!

## 🔧 Troubleshooting

### Model Not Loading?

Check logs in `app/logs/` for errors. Common issues:

**"Model not found"**
- Ensure `ml/models/plant_health_vision_lora/` exists
- Check file permissions

**"CUDA out of memory"**
- Use Ollama backend instead
- Or use smaller quantization (Q4_K_M)

**"Ollama connection refused"**
- Start Ollama: `ollama serve`
- Or backend will auto-fallback to mock

### Training Failed?

**"CUDA out of memory" in Colab**
- Reduce batch size to 1
- Increase gradient accumulation to 8
- Use smaller base model (1B instead of 2B)

**"Dataset download failed"**
- Use manual download links
- Or use custom dataset curator

### Conversion Failed?

**"llama.cpp not found"**
- Script will auto-clone llama.cpp
- May need to install build tools: `apt-get install build-essential`

**"Unsupported model architecture"**
- Check Qwen2-VL is supported in latest llama.cpp
- May need to update llama.cpp: `cd llama.cpp && git pull`

## 📚 Next Steps

### Immediate (Week 1)

- [x] Run Colab notebook
- [ ] Download trained model
- [ ] Deploy to Ollama
- [ ] Test with real plant photos

### Short-term (Week 2-4)

- [ ] Collect user feedback
- [ ] Build custom cannabis dataset
- [ ] Retrain with domain-specific data
- [ ] Performance monitoring

### Long-term (Month 2+)

- [ ] Add vision capabilities to mock data
- [ ] Expand to pest/disease detection
- [ ] Multi-model ensemble
- [ ] Mobile-optimized inference

## 🤝 Contributing

To add more training data:

1. Use the dataset curator tool
2. Submit curated examples via PR
3. Examples get added to next training run

## 📞 Support

Issues or questions?

- Check `docs/user_stories.md` for context
- Review `implementation_plan.md` for details
- Open an issue with model logs

---

**Happy Growing! 🌱**

*Automated by CultivAR AI Team*
