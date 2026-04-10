# Benchmark Report:

## Models Evaluated
- **Base Model**
- **Fine-Tuned Model**
- **Quantized 4-bit Model**
- **GGUF (CPU Inference)**

---

## Evaluation Setup

| Metric            | Description |
|------------------|------------|
| Tokens/sec       | Throughput (higher is better) |
| Latency (sec)    | Response time (lower is better) |
| VRAM (GB)        | GPU memory usage |
| Tasks            | QA, Extraction, Reasoning |

---

## Performance Summary

### Speed (Tokens/sec)

| Model           | QA   | Extraction | Reasoning |
|----------------|------|------------|-----------|
| Base           | 26.8 | 33.1       | 35.7      |
| Fine-Tuned     | 5.2  | 5.0        | 4.6       |
| Quantized 4bit | 17.1 | 16.4       | 13.6      |
| GGUF (CPU)     | 4.0  | 5.3        | 7.7       |

**Observation:**
- Base model is fastest
- Quantized model offers good balance
- Fine-tuned and GGUF are slower

---

### Latency (seconds)

| Model           | QA    | Extraction | Reasoning |
|----------------|-------|------------|-----------|
| Base           | 2.24  | 0.51       | 1.68      |
| Fine-Tuned     | 11.63 | 3.39       | 12.95     |
| Quantized 4bit | 3.50  | 1.03       | 4.40      |
| GGUF (CPU)     | 15.03 | 3.02       | 7.78      |

**Observation:**
- Base model has lowest latency
- Quantized model is acceptable for production
- GGUF is slow but CPU-friendly

---

### Memory Usage (VRAM)

| Model           | VRAM (GB) |
|----------------|----------|
| Base           | 2.2      |
| Fine-Tuned     | 0.82     |
| Quantized 4bit | 0.77     |
| GGUF (CPU)     | 0.0      |

**Observation:**
- Quantization significantly reduces memory
- GGUF enables **CPU-only inference**

---

## Task-wise Output Quality

### 1. QA Task
- All models produce reasonable answers
- Fine-tuned & quantized responses are more **aligned with HR tone**
- Base model is more **generic**

---

### 2. Extraction Task
- All models perform **perfectly**
- Structured information extraction is consistent across models

---

### 3. Reasoning Task
- Responses show **hallucination risk**
- Some outputs suggest **overly extreme actions** (e.g., immediate termination)
- GGUF model provides slightly more **step-by-step reasoning**
---

## Key Insights

- **Quantized 4-bit model is the best trade-off**
  - Good speed
  - Low memory
  - Maintains quality

- **Fine-tuning improves domain alignment**
  - But reduces speed significantly

- **Base model is fastest but less specialized**

- **GGUF enables deployment without GPU**
  - Ideal for edge or local systems

---

## Limitations

- Small evaluation dataset
- Limited prompt diversity
- No quantitative accuracy scoring (only qualitative)

---

## Future Improvements

- Add **automated evaluation metrics**
  - Accuracy
  - Faithfulness
  - Hallucination rate

- Expand test dataset
- Improve reasoning prompts
- Add RAG-based evaluation

---

## Conclusion

For an HR assistant system:

- ✅ Use **Quantized 4-bit model** for production
- ✅ Use **Fine-tuned model** when accuracy is critical
- ✅ Use **GGUF** for CPU-only environments

---