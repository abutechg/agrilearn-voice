from argparse import ArgumentParser
from pathlib import Path
import json
import os
import shlex
import subprocess
import time

import requests
from faster_whisper import WhisperModel


parser = ArgumentParser(description="Compare ASR models on one shared manifest.")
parser.add_argument("--manifest", default="benchmark/fixed_custom/manifest.json")
parser.add_argument("--output", default="benchmark/results.json")
parser.add_argument("--sahara-language", default=os.getenv("SAHARA_LANGUAGE", "en"))
parser.add_argument("--whisper-command", default=os.getenv("WHISPER_COMMAND", "__builtin_whisper__"))
parser.add_argument("--third-command", default=os.getenv("THIRD_MODEL_COMMAND", ""))
parser.add_argument("--limit", type=int, default=0, help="Process only the first N samples; 0 means all.")
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = os.getenv("SAHARA_ENDPOINT", "https://infer.voice.intron.io/file/v1/upload/sync")
whisper_model = None


def normalize(text):
    return " ".join("".join(character.lower() if character.isalnum() else " " for character in str(text or "")).split())


def edit_distance(left, right):
    previous = list(range(len(right) + 1))
    for row, left_char in enumerate(left, start=1):
        current = [row]
        for column, right_char in enumerate(right, start=1):
            current.append(min(current[-1] + 1, previous[column] + 1, previous[column - 1] + (left_char != right_char)))
        previous = current
    return previous[-1]


def rate(reference, hypothesis, unit):
    reference = normalize(reference)
    hypothesis = normalize(hypothesis)
    expected = reference.split() if unit == "word" else list(reference.replace(" ", ""))
    actual = hypothesis.split() if unit == "word" else list(hypothesis.replace(" ", ""))
    return edit_distance(expected, actual) / len(expected) if expected else float(bool(actual))


def transcribe_sahara(audio_path):
    api_key = os.getenv("INTRON_API_KEY")
    if not api_key:
        raise RuntimeError("INTRON_API_KEY is not configured")
    with audio_path.open("rb") as audio_file:
        response = requests.post(
            ENDPOINT,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"audio_file_blob": (audio_path.name, audio_file, "audio/wav")},
            data={"audio_file_name": audio_path.name, "use_language_asr_input": args.sahara_language},
            timeout=180,
        )
    response.raise_for_status()
    result = response.json()
    transcript = result.get("data", {}).get("audio_transcript") or result.get("transcript") or result.get("text")
    if not transcript:
        raise RuntimeError("Sahara returned no transcript")
    return transcript


def transcribe_command(audio_path, template):
    if not template:
        raise RuntimeError("model command is not configured")
    if template == "__builtin_whisper__":
        global whisper_model
        if whisper_model is None:
            whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = whisper_model.transcribe(str(audio_path), beam_size=5, language="yo")
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        if not transcript:
            raise RuntimeError("Whisper returned no transcript")
        return transcript
    command_parts = shlex.split(template, posix=False)
    command_parts = [part.strip('"') for part in command_parts]
    command_parts = [str(audio_path) if part == "{file}" else part for part in command_parts]
    result = subprocess.run(command_parts, cwd=ROOT, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"command exited {result.returncode}")
    if not result.stdout.strip():
        raise RuntimeError("model command returned no transcript")
    return result.stdout.strip()


manifest_path = ROOT / args.manifest
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
if not manifest:
    raise SystemExit("Manifest must contain at least one sample")
if args.limit:
    manifest = manifest[:args.limit]

models = [
    ("sahara", "Sahara/Intron", transcribe_sahara),
    ("whisper", "Whisper", lambda path: transcribe_command(path, args.whisper_command)),
    ("third", "Third model", lambda path: transcribe_command(path, args.third_command)),
]
result = {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "manifest": args.manifest, "models": {}}

for model_id, label, transcribe in models:
    samples = []
    for item in manifest:
        started = time.perf_counter()
        try:
            transcript = transcribe(ROOT / item["audio"])
            samples.append({
                "id": item["id"],
                "reference": item["reference"],
                "transcript": transcript,
                "wer": rate(item["reference"], transcript, "word"),
                "cer": rate(item["reference"], transcript, "char"),
                "latencyMs": round((time.perf_counter() - started) * 1000),
            })
        except Exception as error:
            samples.append({"id": item["id"], "reference": item["reference"], "error": str(error), "latencyMs": round((time.perf_counter() - started) * 1000)})
    successful = [sample for sample in samples if "error" not in sample]
    result["models"][model_id] = {
        "label": label,
        "samples": samples,
        "summary": {
            "total": len(samples),
            "successful": len(successful),
            "failures": len(samples) - len(successful),
            "wer": sum(sample["wer"] for sample in successful) / len(successful) if successful else None,
            "cer": sum(sample["cer"] for sample in successful) / len(successful) if successful else None,
            "meanLatencyMs": sum(sample["latencyMs"] for sample in successful) / len(successful) if successful else None,
        },
    }

output_path = ROOT / args.output
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {output_path}")