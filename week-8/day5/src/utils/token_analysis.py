# utils/token_analysis.py

import json
import os
import matplotlib.pyplot as plt
from transformers import AutoTokenizer

# PATH SETUP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # src/utils/
SRC_DIR = os.path.dirname(BASE_DIR)                     # src/
DATA_DIR = os.path.join(SRC_DIR, "data")

TRAIN_PATH = os.path.join(DATA_DIR, "train.jsonl")

# LOAD TOKENIZER

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")

# ANALYSIS

lengths = []

with open(TRAIN_PATH, "r") as f:
    for line in f:
        data = json.loads(line)
        text = data["instruction"] + data["input"] + data["output"]

        tokens = tokenizer.encode(text)
        lengths.append(len(tokens))

# STATS

print("\n📊 TOKEN STATS")
print(f"Total samples: {len(lengths)}")
print(f"Max tokens: {max(lengths)}")
print(f"Min tokens: {min(lengths)}")
print(f"Average tokens: {sum(lengths)/len(lengths):.2f}")

# HISTOGRAM

plt.figure(figsize=(10, 6))
plt.hist(lengths, bins=50)
plt.title("Token Length Distribution")
plt.xlabel("Token Count")
plt.ylabel("Frequency")
plt.grid()

plt.show()

# OUTLIERS

outliers = [l for l in lengths if l > 1024]
print(f"\n⚠️ Samples >1024 tokens: {len(outliers)}")