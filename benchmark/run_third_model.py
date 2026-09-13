import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

"""
Third benchmark model: Meta MMS (Massively Multilingual Speech).

MMS supports 1,100+ languages including Yoruba (yo).
Model: facebook/mms-1b-all

NOTE: This script requires transformers and torch.
Install with:
  pip install transformers torch torchaudio

The first run will download the model (~1 GB).
"""

import json
import time
from argparse import ArgumentParser
from pathlib import Path

import soundfile as sf
import numpy as np

parser = ArgumentParser(description="Run Meta MMS ASR on the fixed benchmark subset.")
parser.add_argument("--manifest", default="fixed_yoruba_subset/manifest.json")
parser.add_argument("--output", default="predictions/meta_mms.json")
parser.add_argument("--language", default="yor")  # MMS uses ISO 639-3 codes; Yoruba = "yor"
args = parser.parse_args()

# Lazy import so the script gives a clear error if torch isn't installed
try:
    from transformers import Wav2Vec2ForCTC, AutoProcessor
    import torch
except ImportError:
    raise SystemExit(
        "Meta MMS requires transformers and torch.\n"
        "Install with: pip install transformers torch torchaudio"
    )

MODEL_ID = "facebook/mms-1b-all"
TARGET_SR = 16000

print(f"Loading Meta MMS model ({MODEL_ID})...")
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

# Set target language adapter
processor.tokenizer.set_target_lang(args.language)
model.load_adapter(args.language)
model.eval()

print(f"Language adapter loaded: {args.language}")

with open(args.manifest, "r", encoding="utf-8") as file:
    records = json.load(file)

predictions = []

for index, record in enumerate(records, start=1):
    audio_path = Path(record["audio"])
    print(f"[{index}/{len(records)}] Transcribing {audio_path.name}...")

    start_time = time.time()
    try:
        audio_array, sample_rate = sf.read(audio_path, dtype="float32")

        # Resample to 16kHz if needed
        if sample_rate != TARGET_SR:
            # Simple linear resample
            duration = len(audio_array) / sample_rate
            num_samples = int(duration * TARGET_SR)
            audio_array = np.interp(
                np.linspace(0, len(audio_array) - 1, num_samples),
                np.arange(len(audio_array)),
                audio_array,
            ).astype(np.float32)

        inputs = processor(
            audio_array,
            sampling_rate=TARGET_SR,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model(**inputs).logits

        predicted_ids = torch.argmax(outputs, dim=-1)
        transcript = processor.batch_decode(predicted_ids)[0].strip()

        duration = time.time() - start_time
        predictions.append({
            "id": record["id"],
            "reference": record["reference"],
            "prediction": transcript,
            "model": "Meta MMS (mms-1b-all)",
            "language": args.language,
            "duration": duration,
        })
        print(f"  Done in {duration:.1f}s — {transcript[:80]}")

    except Exception as error:
        duration = time.time() - start_time
        print(f"  Error: {error}")
        predictions.append({
            "id": record["id"],
            "reference": record["reference"],
            "prediction": "",
            "model": "Meta MMS (mms-1b-all)",
            "error": str(error),
            "duration": duration,
        })

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
with open(args.output, "w", encoding="utf-8") as file:
    json.dump(predictions, file, ensure_ascii=False, indent=2)

successful = [p for p in predictions if "error" not in p]
print(f"\nMeta MMS predictions saved to {args.output}")
print(f"  Total: {len(predictions)} | Successful: {len(successful)} | Failed: {len(predictions) - len(successful)}")
