import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json
import re
from pathlib import Path

from jiwer import wer, cer


def normalize(text):
    text = (text or "").lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

for path in sorted(Path("predictions").glob("*.json")):
    with open(path, "r", encoding="utf-8") as file:
        predictions = json.load(file)
    references = [normalize(item["reference"]) for item in predictions]
    hypotheses = [normalize(item["prediction"]) for item in predictions]
    result = {
        "model": Path(path).stem,
        "samples": len(predictions),
        "wer": wer(references, hypotheses),
        "cer": cer(references, hypotheses),
    }
    print(f"{result['model']}: {result['samples']} samples | WER={result['wer']:.4f} | CER={result['cer']:.4f}")
