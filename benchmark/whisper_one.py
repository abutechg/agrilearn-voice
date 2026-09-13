from argparse import ArgumentParser

from faster_whisper import WhisperModel


parser = ArgumentParser()
parser.add_argument("audio")
parser.add_argument("--model", default="tiny")
parser.add_argument("--language", default="yo")
args = parser.parse_args()

model = WhisperModel(args.model, device="cpu", compute_type="int8")
segments, _ = model.transcribe(args.audio, beam_size=5, language=args.language)
print(" ".join(segment.text.strip() for segment in segments).strip())