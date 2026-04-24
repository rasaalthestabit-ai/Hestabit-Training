import json
import os
import random

# PATH SETUP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # src/utils/
SRC_DIR = os.path.dirname(BASE_DIR)                     # src/
DATA_DIR = os.path.join(SRC_DIR, "data")

RAW_PATH = os.path.join(DATA_DIR, "raw_data.jsonl")
CLEANED_FULL = os.path.join(DATA_DIR, "cleaned_data.jsonl")

TRAIN_PATH = os.path.join(DATA_DIR, "train.jsonl")
VAL_PATH = os.path.join(DATA_DIR, "val.jsonl")


# CLEAN FUNCTION

def clean_data(input_path, output_path, max_char_length=2000):
    seen = set()
    cleaned = []

    with open(input_path, "r") as f:
        for line in f:
            data = json.loads(line)

            instr = data.get("instruction", "").strip()
            inp = data.get("input", "").strip()
            out = data.get("output", "").strip()

            # Remove empty
            if not instr or not out:
                continue

            # Remove duplicates
            key = instr + inp + out
            if key in seen:
                continue
            seen.add(key)

            # Remove too long
            if len(key) > max_char_length:
                continue

            cleaned.append({
                "instruction": instr,
                "input": inp,
                "output": out
            })

    with open(output_path, "w") as f:
        for item in cleaned:
            f.write(json.dumps(item) + "\n")

    print(f"✅ Cleaned dataset: {len(cleaned)} samples")
    return cleaned


# SPLIT FUNCTION

def split_data(cleaned_data, train_path, val_path, split_ratio=0.9):
    random.shuffle(cleaned_data)

    split_idx = int(split_ratio * len(cleaned_data))
    train = cleaned_data[:split_idx]
    val = cleaned_data[split_idx:]

    with open(train_path, "w") as f:
        for item in train:
            f.write(json.dumps(item) + "\n")

    with open(val_path, "w") as f:
        for item in val:
            f.write(json.dumps(item) + "\n")

    print(f"✅ Train samples: {len(train)}")
    print(f"✅ Val samples: {len(val)}")


# RUN

if __name__ == "__main__":
    cleaned_data = clean_data(RAW_PATH, CLEANED_FULL)
    split_data(cleaned_data, TRAIN_PATH, VAL_PATH)