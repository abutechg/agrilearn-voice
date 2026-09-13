# Custom agricultural evaluation set

This is the recommended AfriSwitch alternative for the competition benchmark. It is small, domain-specific, and reproducible if collected carefully.

## Target set

- 30-50 short clips, 5-15 seconds each
- At least 8 speakers, with speaker IDs excluded from the public manifest
- Real agricultural questions from target users
- Yoruba-English, or the language pair the product will claim to support
- A held-out evaluation set never used to tune the matcher or prompts

## Collection rules

Ask each participant for explicit permission to record and use the clip for this evaluation. Do not record names, phone numbers, faces, or precise locations. Let the speaker answer a prompt in their own words. Have a second reviewer correct the transcript and mark code-switched words.

Put only consented WAV files and this metadata file in `benchmark/custom_source/`:

```csv
id,audio,reference,languagePair,topic,consent
agri-001,agri-001.wav,How do I prepare my soil before planting maize?,Yoruba-English,Soil preparation,yes
```

Do not include synthetic fixtures in the evaluation set. Do not publish raw recordings without permission.

## Build the shared dataset

```powershell
& ".\benchmark\.venv\Scripts\python.exe" ".\benchmark\prepare_custom_subset.py"
```

This creates `benchmark/fixed_custom/manifest.json`. Sahara, Whisper, and the third model must all use that same manifest and audio directory.

For the one-file Whisper adapter used by the JavaScript benchmark runner, set this process variable in PowerShell:

```powershell
$env:WHISPER_COMMAND = '".\benchmark\.venv\Scripts\python.exe" ".\benchmark\whisper_one.py" {file}'
```

## About AI-generated answers and speech

The draft answer bank in `benchmark/agriculture_answer_bank.json` can help prepare controlled responses and recording prompts. A human with agricultural knowledge must review each answer before production use; the entries are intentionally marked `draft-review-needed`.

Open-source text-to-speech tools such as Piper can generate audio for software smoke tests. That audio is synthetic and must not be mixed into the competition evaluation set. For model comparison, use real consented speakers so the result measures recognition of the target community rather than recognition of a TTS voice.

To generate synthetic Yoruba answer voice-overs from the draft answer bank, install the local dependencies and run:

```powershell
& ".\benchmark\.venv\Scripts\python.exe" -m pip install torch transformers sentencepiece
& ".\benchmark\.venv\Scripts\python.exe" ".\benchmark\generate_voiceovers.py"
```

The default model is `facebook/mms-tts-yor`. The output is placed in `benchmark/synthetic_voiceovers/` and marked `synthetic: true`. Use it for app demos and pipeline checks only, never for WER/CER competition scores.