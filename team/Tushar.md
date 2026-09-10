# Tushar — ML / AI

> **Role:** Machine Learning Engineer
> **Primary Workspace:** `ml-training/`, `backend/app/ml/`

---

## 🎯 What You Own

| Area                     | Directories / Files                                    |
|--------------------------|--------------------------------------------------------|
| **Training Notebooks**   | `ml-training/` (Jupyter notebooks for Google Colab)    |
| **Training Datasets**    | `ml-training/datasets/`                                |
| **ML Module (Backend)**  | `backend/app/ml/` (model loading, inference, utilities)|
| **Trained Models**       | `backend/app/ml/models/` (exported `.h5`, `.pt`, etc.) |

---

## 📋 Key Responsibilities

### Phase 1 — Data & Research (Weeks 1–2)
- [ ] Research and collect training datasets for civic complaint classification
  - [ ] Image dataset: road damage, garbage, water leaks, electrical, other (aim for ~500+ images per class)
  - [ ] Text dataset: complaint descriptions mapped to the same 5 categories
- [ ] Set up Google Colab notebooks for training
- [ ] Data cleaning, augmentation, and train/val/test splits
- [ ] Document dataset sources and preprocessing steps

### Phase 2 — Image Classification (Weeks 3–4)
- [ ] Fine-tune **MobileNetV2** on the 5-class image dataset
  - [ ] Transfer learning from ImageNet weights
  - [ ] Data augmentation (rotation, flip, brightness, zoom)
  - [ ] Train on Google Colab (free GPU)
- [ ] Evaluate: target **≥ 80% accuracy** on validation set
- [ ] Export model as `.h5` or `.tflite` for CPU inference
- [ ] Write inference function in `backend/app/ml/` that loads model and returns `{ category, confidence }`

### Phase 3 — Text Classification (Weeks 5–6)
- [ ] Fine-tune **DistilBERT** on the 5-class text dataset
  - [ ] Use Hugging Face `transformers` + `datasets` library
  - [ ] Tokenizer setup, training loop on Colab
- [ ] Evaluate: target **≥ 85% accuracy** on validation set
- [ ] Export model (saved model or ONNX)
- [ ] Write inference function in `backend/app/ml/` that returns `{ category, confidence }`

### Phase 4 — Integration & Polish (Weeks 7–8)
- [ ] Coordinate with Sairaj to integrate into FastAPI endpoints
  - [ ] `POST /api/classify/image` → accepts image, returns category + confidence
  - [ ] `POST /api/classify/text` → accepts text, returns category + confidence
- [ ] Ensemble/fusion logic: combine image + text predictions for higher accuracy
- [ ] Model performance monitoring (log predictions, track accuracy drift)
- [ ] (Optional) LLM integration via adapter pattern for complaint summarization

---

## 🔗 Coordination Points

| With       | What                                                                 |
|------------|----------------------------------------------------------------------|
| **Sairaj** | Agree on model input/output format, endpoint contracts, and where models are stored (`backend/app/ml/models/`) |
| **Sufiyan**| Provide classification results format so frontend can display category badges and confidence scores |

---

## 🧪 Model Specs

| Model         | Task                | Architecture      | Size   | Target Accuracy | Inference Device |
|---------------|---------------------|--------------------|--------|-----------------|------------------|
| Image Classifier | 5-class image sort | MobileNetV2 (fine-tuned) | ~14 MB | ≥ 80% | CPU |
| Text Classifier  | 5-class text sort  | DistilBERT (fine-tuned)  | ~250 MB | ≥ 85% | CPU |

### Categories (5 classes)

1. 🛣️ **Road / Pothole**
2. 🗑️ **Garbage / Sanitation**
3. 💧 **Water Supply / Leak**
4. ⚡ **Electrical / Street Light**
5. 📦 **Other**

---

## 📚 Learning Resources

- [TensorFlow Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [Hugging Face DistilBERT Fine-Tuning](https://huggingface.co/docs/transformers/training)
- [Google Colab Tips](https://colab.research.google.com/)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)

---

## 📝 Personal Notes

> Use this space for your own notes, blockers, questions, or ideas.
> This file is gitignored — it's your private scratchpad.

- 

