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
| Base           | 32.6 | 33.3       | 31.0      |
| Fine-Tuned     | 12.9 | 4.7        | 9.5       |
| Quantized 4bit | 6.4  | 7.6        | 5.7       |
| GGUF (CPU)     | 3.0  | 3.6        | 2.9       |

**Observation:**
- Base model remains the fastest across all tasks
- Fine-tuned model shows strong drop in extraction speed
- Quantized model is slower but consistent
- GGUF is the slowest due to CPU-bound execution

---

### Latency (seconds)

| Model           | QA    | Extraction | Reasoning |
|----------------|-------|------------|-----------|
| Base           | 1.84  | 0.51       | 1.93      |
| Fine-Tuned     | 1.86  | 6.44       | 3.25      |
| Quantized 4bit | 9.41  | 2.25       | 10.59     |
| GGUF (CPU)     | 7.76  | 8.01       | 8.88      |

**Observation:**
- Base model has the lowest and most stable latency
- Fine-tuned model performs well in QA but poorly in extraction
- Quantized model introduces very high latency, especially in reasoning
- GGUF shows consistently high latency across tasks

---

### Memory Usage (VRAM)

| Model           | VRAM (GB) |
|----------------|----------|
| Base           | 2.2      |
| Fine-Tuned     | 0.82     |
| Quantized 4bit | 0.77     |
| GGUF (CPU)     | 0.0      |

**Observation:**
- Fine-tuning and quantization reduce memory usage by ~60–65%
- Quantized model is the most memory-efficient GPU option
- GGUF completely removes GPU dependency

---

## Task-wise Output Quality

### 1. QA Task
- All models generate valid answers
- Fine-tuned model provides better **HR-specific alignment**
- Base model is more **general-purpose**
- Quantized model maintains acceptable quality despite compression

---

### 2. Extraction Task
- Base model performs fastest and most reliably
- Fine-tuned model shows **performance degradation (latency spike)**
- Output structure remains consistent across all models

---

### 3. Reasoning Task
- All models show **hallucination risk**
- Quantized model struggles with long reasoning chains (high latency)
- GGUF produces slower but sometimes more **step-wise outputs**
- Fine-tuned model improves domain tone but not reasoning robustness

---

## Key Insights

- **Base model is best for raw performance**
  - Highest throughput
  - Lowest latency
  - Highest memory usage

- **Fine-tuned model improves domain alignment**
  - Strong for QA
  - Significant slowdown in extraction tasks

- **Quantized 4-bit model prioritizes efficiency**
  - Very low VRAM usage
  - High latency makes it less suitable for real-time systems

- **GGUF enables CPU-only deployment**
  - Useful for edge environments
  - Not suitable for latency-sensitive applications

---

## Limitations

- Small evaluation dataset
- Limited diversity in prompts
- No quantitative scoring (accuracy, F1, etc.)
- No stress testing under concurrent load

---

## Future Improvements

- Introduce **automated evaluation metrics**
  - Accuracy
  - Hallucination rate
  - Response consistency

- Expand dataset size and diversity
- Optimize fine-tuning pipeline for extraction tasks
- Improve quantization strategy (e.g., AWQ / GPTQ tuning)
- Add RAG-based benchmarking for real-world scenarios

---

## Conclusion

For an HR assistant system:

- Use **Base Model** when performance is critical and GPU is available
- Use **Fine-Tuned Model** for better domain alignment (QA-focused use cases)
- Use **Quantized 4-bit Model** when memory is constrained but latency is acceptable
- Use **GGUF** for CPU-only deployments or offline environments