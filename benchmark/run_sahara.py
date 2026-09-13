import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
import json
import time
import requests
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser(description="Run Sahara/Intron ASR on the fixed benchmark subset.")
parser.add_argument("--manifest", default="fixed_yoruba_subset/manifest.json")
parser.add_argument("--output", default="predictions/sahara.json")
parser.add_argument("--language", default=os.getenv("SAHARA_LANGUAGE", "yo"))
args = parser.parse_args()

API_KEY = os.environ.get("INTRON_API_KEY")
if not API_KEY:
    raise SystemExit(
        "INTRON_API_KEY is not set. "
        "Set it via: $env:INTRON_API_KEY='your_key' (PowerShell) "
        "or set INTRON_API_KEY=your_key (cmd)"
    )

ENDPOINT = os.getenv(
    "SAHARA_ENDPOINT",
    "https://infer.voice.intron.io/file/v1/upload/sync",
)

with open(args.manifest, "r", encoding="utf-8") as file:
    records = json.load(file)

predictions = []

for index, record in enumerate(records, start=1):
    audio_path = Path(record["audio"])
    print(f"[{index}/{len(records)}] Sending {audio_path.name}...")

    start_time = time.time()
    try:
        with open(audio_path, "rb") as audio_file:
            files = {
                "audio_file_blob": (
                    audio_path.name,
                    audio_file,
                    "audio/wav",
                )
            }
            data = {
                "audio_file_name": audio_path.name,
                "use_language_asr_input": args.language,
            }
            response = requests.post(
                ENDPOINT,
                headers={"Authorization": f"Bearer {API_KEY}"},
                files=files,
                data=data,
                timeout=180,
            )

        duration = time.time() - start_time
        result = response.json()

        if not response.ok:
            print(f"  API error ({response.status_code}): {result}")
            predictions.append({
                "id": record["id"],
                "reference": record["reference"],
                "prediction": "",
                "model": "Sahara/Intron",
                "error": f"HTTP {response.status_code}",
                "duration": duration,
            })
            continue

        transcript = (
            result.get("data", {}).get("audio_transcript", "")
            or result.get("transcript", "")
            or result.get("text", "")
            or result.get("data", {}).get("transcript", "")
            or result.get("data", {}).get("text", "")
        )

        predictions.append({
            "id": record["id"],
            "reference": record["reference"],
            "prediction": transcript,
            "model": "Sahara/Intron",
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
            "model": "Sahara/Intron",
            "error": str(error),
            "duration": duration,
        })

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
with open(args.output, "w", encoding="utf-8") as file:
    json.dump(predictions, file, ensure_ascii=False, indent=2)

successful = [p for p in predictions if "error" not in p]
print(f"\nSahara predictions saved to {args.output}")
print(f"  Total: {len(predictions)} | Successful: {len(successful)} | Failed: {len(predictions) - len(successful)}")
