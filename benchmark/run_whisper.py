import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from argparse import ArgumentParser
from faster_whisper import WhisperModel
from pathlib import Path
import json
import time

parser = ArgumentParser(description="Run Whisper ASR on the fixed benchmark subset.")
parser.add_argument("--manifest", default="fixed_yoruba_subset/manifest.json")
parser.add_argument("--model", default="large-v3")
parser.add_argument("--output", default="predictions/whisper_large_v3.json")
args = parser.parse_args()

MODEL_NAME = args.model
print(f"Loading Whisper model {MODEL_NAME}...")
model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")

with open(args.manifest, "r", encoding="utf-8") as file:
    records = json.load(file)

predictions = []
for index, record in enumerate(records, start=1):
    audio_path = Path(record["audio"])
    print(f"[{index}/{len(records)}] Transcribing {audio_path.name}...")
    start_time = time.time()
    segments, info = model.transcribe(str(audio_path), beam_size=5, language="yo")
    transcript = " ".join(segment.text.strip() for segment in segments).strip()
    duration = time.time() - start_time
    predictions.append({
        "id": record["id"],
        "reference": record["reference"],
        "prediction": transcript,
        "model": MODEL_NAME,
        "language": info.language,
        "duration": duration,
    })
    print(f"  Done in {duration:.1f}s — {transcript[:80]}")

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
with open(args.output, "w", encoding="utf-8") as file:
    json.dump(predictions, file, ensure_ascii=False, indent=2)

successful = [p for p in predictions if p.get("prediction")]
print(f"\nWhisper predictions saved to {args.output}")
print(f"  Total: {len(predictions)} | With transcript: {len(successful)}")
