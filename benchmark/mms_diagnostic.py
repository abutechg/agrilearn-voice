"""
Meta MMS diagnostic — writes progress directly to a log file so output is visible.
"""
import sys
import os
import time
import json
import traceback
from pathlib import Path

LOG = Path("mms_test.log")
LOG.write_text("", encoding="utf-8")  # clear

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
        f.flush()
    print(msg, flush=True)

log(f"=== MMS Diagnostic start {time.ctime()} ===")

MODEL_ID = "facebook/mms-1b-all"
log(f"Loading {MODEL_ID}...")

t0 = time.time()
try:
    from transformers import Wav2Vec2ForCTC, AutoProcessor
    import torch
    import soundfile as sf
    log(f"Imports OK in {time.time()-t0:.1f}s")

    t1 = time.time()
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    log(f"Processor loaded in {time.time()-t1:.1f}s")

    t2 = time.time()
    model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
    log(f"Model loaded in {time.time()-t2:.1f}s")

    if hasattr(processor.tokenizer, "set_target_lang"):
        processor.tokenizer.set_target_lang("yor")
        model.load_adapter("yor")
        log("Yoruba adapter loaded")
    else:
        log("No adapter API — using base model")

    model.eval()
    log(f"Model ready. Total load time: {time.time()-t0:.1f}s")

    # Single sample inference test
    manifest = json.load(open("fixed_yoruba_subset/manifest.json", encoding="utf-8"))
    rec = manifest[0]
    audio_path = Path(rec["audio"])
    log(f"Reading audio: {audio_path.name}")

    audio, sr = sf.read(audio_path, dtype="float32")
    log(f"Audio loaded: {len(audio)} samples @ {sr}Hz, duration={len(audio)/sr:.2f}s")

    t3 = time.time()
    log("Running inference...")
    inputs = processor(audio, sampling_rate=sr, return_tensors="pt")
    log(f"Input tensor shape: {inputs.input_values.shape}")

    with torch.no_grad():
        logits = model(**inputs).logits

    log(f"Logits shape: {logits.shape}")
    ids = torch.argmax(logits, dim=-1)
    text = processor.batch_decode(ids)[0].strip()
    elapsed = time.time() - t3
    log(f"Inference done in {elapsed:.1f}s => '{text[:100]}'")

except Exception as e:
    log(f"ERROR: {e}")
    log(traceback.format_exc())

log("=== Done ===")
