from argparse import ArgumentParser
from pathlib import Path
import json

import soundfile as sf
import torch
from transformers import AutoTokenizer, VitsModel


parser = ArgumentParser(description="Generate synthetic voice-over WAV files from the agriculture answer bank.")
parser.add_argument("--model", default="facebook/mms-tts-yor", help="Hugging Face TTS model, default is Yoruba MMS.")
parser.add_argument("--answers", default="benchmark/agriculture_answer_bank.json")
parser.add_argument("--output", default="benchmark/synthetic_voiceovers")
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
answers = json.loads((root / args.answers).read_text(encoding="utf-8"))
output_dir = root / args.output
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Loading {args.model}...")
tokenizer = AutoTokenizer.from_pretrained(args.model)
model = VitsModel.from_pretrained(args.model)
model.eval()
records = []

for index, item in enumerate(answers, start=1):
    print(f"Generating {index}/{len(answers)}: {item['id']}")
    inputs = tokenizer(item["answer"], return_tensors="pt")
    with torch.no_grad():
        waveform = model(**inputs).waveform.squeeze().cpu().numpy()
    audio_path = output_dir / f"{item['id']}.wav"
    sf.write(audio_path, waveform, model.config.sampling_rate)
    records.append({
        "id": item["id"],
        "audio": str(audio_path.relative_to(root)).replace("\\", "/"),
        "reference": item["answer"],
        "question": item["question"],
        "languagePair": "Yoruba synthetic voice-over",
        "topic": "Agricultural answer voice-over",
        "dataset": "Synthetic TTS voice-over; pipeline/demo only",
        "synthetic": True,
    })

(output_dir / "manifest.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Created {len(records)} synthetic voice-overs in {output_dir}")