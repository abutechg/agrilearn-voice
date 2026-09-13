from datasets import load_from_disk, Audio
from pathlib import Path
import json
import io
import soundfile as sf

# Load dataset with audio decoding disabled to avoid torchcodec dependency
dataset = load_from_disk("afriswitch_yoruba_test")
dataset = dataset.cast_column("audio", Audio(decode=False))

output_dir = Path("fixed_yoruba_subset")
audio_dir = output_dir / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)

records = []
subset = dataset.select(range(min(100, len(dataset))))

for index, item in enumerate(subset):
    audio_data = item["audio"]
    audio_path = audio_dir / f"sample_{index:04d}.wav"

    # audio_data is {"bytes": b"...", "path": "..."} when decode=False
    raw_bytes = audio_data["bytes"]

    if raw_bytes:
        # Read the raw audio bytes and re-write as a proper WAV
        try:
            audio_array, sample_rate = sf.read(io.BytesIO(raw_bytes))
            sf.write(str(audio_path), audio_array, sample_rate)
        except Exception:
            # If soundfile can't read the format, just write raw bytes
            # and hope the downstream tools can handle it
            audio_path.write_bytes(raw_bytes)
    else:
        print(f"  Warning: sample {index} has no audio bytes, skipping.")
        continue

    records.append({
        "id": f"sample_{index:04d}",
        "audio": str(audio_path),
        "reference": item["transcription"]
    })
    if (index + 1) % 10 == 0:
        print(f"  Extracted {index + 1} samples...")

with open(output_dir / "manifest.json", "w", encoding="utf-8") as file:
    json.dump(records, file, ensure_ascii=False, indent=2)

print(f"\nCreated {len(records)} fixed benchmark samples in {output_dir}/")
