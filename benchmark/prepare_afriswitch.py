from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path
import json

import soundfile as sf
from datasets import load_dataset


parser = ArgumentParser(description="Create one fixed AfriSwitch evaluation manifest.")
parser.add_argument("--language", default="yoruba")
parser.add_argument("--limit", type=int, default=20)
parser.add_argument("--output", default="benchmark/fixed_afriswitch")
args = parser.parse_args()

repo_root = Path(__file__).resolve().parents[1]
dataset_dir = repo_root / "benchmark" / "afriswitch" / "data" / args.language
parquet_files = sorted(dataset_dir.glob("test-*.parquet"))
if not parquet_files:
    raise SystemExit(
        f"No downloaded parquet files found in {dataset_dir}. "
        "Download AfriSwitch payload files first."
    )

print(f"Loading {args.language} AfriSwitch data from {len(parquet_files)} parquet file(s)...")
dataset = load_dataset(
    "parquet",
    data_files=[str(file) for file in parquet_files],
    split="train",
    streaming=True,
)

output_dir = repo_root / args.output
audio_dir = output_dir / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
records = []

for index, item in enumerate(dataset):
    if index >= args.limit:
        break
    audio = item["audio"]
    audio_path = audio_dir / f"{index:04d}.wav"
    if audio.get("bytes"):
        audio_path.write_bytes(audio["bytes"])
    elif audio.get("path"):
        source_path = Path(audio["path"])
        if not source_path.is_absolute():
            source_path = repo_root / source_path
        audio_path.write_bytes(source_path.read_bytes())
    else:
        raise ValueError(f"Sample {index} has no audio bytes or path")

    records.append({
        "id": f"afriswitch-{args.language}-{index:04d}",
        "audio": str(audio_path.relative_to(repo_root)).replace("\\", "/"),
        "reference": item["transcription"],
        "languagePair": f"{args.language.title()}-English",
        "topic": "Agricultural speech benchmark",
        "dataset": "AfriSwitch",
        "synthetic": False,
    })

if not records:
    raise SystemExit("The dataset contained no samples.")

(output_dir / "manifest.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Created {len(records)} shared evaluation samples at {output_dir / 'manifest.json'}")