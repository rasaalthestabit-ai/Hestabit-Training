# Quantisation Report: HR LLM Optimization

## Objective

The purpose of this experiment is to evaluate different quantization techniques in terms of:
- Model size reduction
- Memory (VRAM) usage
- Inference speed
- Output quality compared to FP16 baseline

---

## Quantization Comparison

| Format        | Size (Disk, GB) | VRAM (Load, GB) | Speed (Tokens/sec) | Quality (vs FP16)        |
|--------------|----------------|-----------------|--------------------|--------------------------|
| FP16         | 2.20           | 2.21            | 16.3               | Baseline                 |
| INT8         | 1.24           | 1.24            | 5.5                | Good (Minor drop)        |
| INT4 (NF4)   | 0.77           | 0.77            | 8.2                | Acceptable (Noticeable)  |
| GGUF (q4_0)  | 0.64           | N/A (CPU only)  | Not measured       | Good (Similar to INT4)   |

---

## Observations

### Model Size Reduction
- INT8 reduces model size by approximately 44% compared to FP16.
- INT4 reduces model size by approximately 65%.
- GGUF provides the smallest disk footprint.

This shows that quantization is highly effective for reducing storage requirements.

---

### Memory Efficiency
- FP16 requires the highest VRAM (~2.2 GB).
- INT8 and INT4 significantly reduce VRAM usage.
- GGUF eliminates the need for GPU memory entirely.

This enables deployment on systems with limited hardware resources.

---

### Speed Trade-offs
- FP16 provides the highest inference speed.
- INT4 performs better than INT8 in this setup.
- INT8 shows lower-than-expected speed, likely due to backend or kernel inefficiencies.
- GGUF speed was not measured, as it runs on CPU.

This highlights that lower precision does not always guarantee faster inference.

---

### Output Quality
- FP16 provides the highest quality output (baseline).
- INT8 shows minimal quality degradation.
- INT4 shows a noticeable but acceptable drop in quality.
- GGUF performs similarly to INT4.

There is a clear trade-off between compression level and output quality.

---

## Trade-off Summary

| Format      | Memory Usage | Speed  | Quality | Recommended Use Case                  |
|-------------|-------------|--------|---------|--------------------------------------|
| FP16        | High        | High   | Very High | Training and high-quality inference |
| INT8        | Medium      | Low    | High    | Balanced inference                   |
| INT4 (NF4)  | Low         | Medium | Moderate| Production with limited VRAM         |
| GGUF (q4_0) | Very Low    | Low    | Moderate| CPU-based deployment                 |

---

## Key Insights

- INT4 (NF4) provides the best overall balance between memory, speed, and quality.
- INT8 reduces memory usage but may not provide optimal speed improvements.
- GGUF is well-suited for CPU-only environments and edge deployments.
- FP16 remains the best option when maximum quality is required and resources are available.

---

## Limitations

- GGUF inference speed was not benchmarked.
- Evaluation was performed on a limited set of prompts.
- Output quality was assessed qualitatively rather than using formal metrics.

---

## Future Improvements

- Benchmark GGUF performance on CPU.
- Introduce quantitative evaluation metrics such as:
  - Perplexity
  - BLEU / ROUGE scores
  - Task-specific accuracy
- Evaluate additional quantization methods such as GPTQ and AWQ.

---

## Conclusion

Quantization is an effective technique for reducing model size and memory requirements while maintaining acceptable performance.

- FP16 should be used when quality is the highest priority.
- INT4 (NF4) is the most practical choice for production environments with limited GPU memory.
- GGUF is suitable for CPU-based deployment scenarios.

Careful selection of quantization method depends on the specific constraints and goals of the deployment environment.