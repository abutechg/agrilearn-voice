from argparse import ArgumentParser
from pathlib import Path
import csv
import json
import shutil


parser = ArgumentParser(description="Package a consented custom agricultural evaluation set.")
parser.add_argument("--source", default="benchmark/custom_source")
parser.add_argument("--output", default="benchmark/fixed_custom")
args = parser.parse_args()

repo_root = Path(__file__).resolve().parents[1]
source_dir = repo_root / args.source
metadata_path = source_dir / "metadata.csv"
if not metadata_path.exists():
    raise SystemExit(f"Missing {metadata_path}. Copy consented WAV files and metadata.csv there first.")

output_dir = repo_root / args.output
audio_dir = output_dir / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
records = []

with metadata_path.open(newline="", encoding="utf-8-sig") as file:
    for row in csv.DictReader(file):
        required = ("id", "audio", "reference", "languagePair", "topic", "consent")
        missing = [field for field in required if not row.get(field, "").strip()]
        if missing:
            raise SystemExit(f"{row.get('id', '<unknown>')} is missing: {', '.join(missing)}")
        if row["consent"].strip().lower() not in {"yes", "true"}:
            raise SystemExit(f"{row['id']} is not marked consent=yes")

        source_audio = source_dir / row["audio"]
        if not source_audio.exists():
            raise SystemExit(f"Missing audio for {row['id']}: {source_audio}")
        destination = audio_dir / f"{row['id']}{source_audio.suffix.lower()}"
        shutil.copy2(source_audio, destination)
        records.append({
            "id": row["id"],
            "audio": str(destination.relative_to(repo_root)).replace("\\", "/"),
            "reference": row["reference"],
            "languagePair": row["languagePair"],
            "topic": row["topic"],
            "dataset": "AgriLearn Voice custom evaluation set",
            "synthetic": False,
        })

if not records:
    raise SystemExit("metadata.csv contains no samples")

(output_dir / "manifest.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Created {len(records)} shared evaluation samples at {output_dir / 'manifest.json'}")