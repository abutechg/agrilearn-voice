### Dataset access status

AfriSwitch was checked through the Hugging Face API and the `hf` CLI. The repository reports `gated=manual`; the CLI is not logged in, and an unauthenticated download returns `Access denied. This repository requires approval.` Access is therefore not currently granted or reproducible here. FLEURS Yoruba was also tested, but the Hub dataset download and dataset-viewer row request did not complete successfully.

For pipeline-only validation when real data is unavailable, generate a clearly synthetic English WAV and manifest:

```powershell
powershell -ExecutionPolicy Bypass -File benchmark/generate_pipeline_fixture.ps1
```

The generated manifest contains `synthetic: true`. Do not use this fixture for WER/CER model claims or competition results. Replace it with a consented, licensed real evaluation subset once AfriSwitch access or another verified source is available.

When AfriSwitch access is active and its parquet payload is present under `benchmark/afriswitch/data/`, create the shared model input once:

```powershell
& ".\benchmark\.venv\Scripts\python.exe" ".\benchmark\prepare_afriswitch.py" --language yoruba --limit 20
```

This writes `benchmark/fixed_afriswitch/manifest.json`. Sahara, Whisper, and the third model must all consume that same manifest and audio directory; do not create a different dataset per model. The current checkout contains only repository pointers, not the parquet payload, because AfriSwitch access is still pending.
AgriLearn Voice
AgriLearn Voice is a mobile-friendly agricultural learning assistant. It accepts a short spoken or typed question, transcribes audio through the server-side Intron/Sahara route, and returns a controlled answer from the curated agriculture knowledge base.

## Run locally

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Enable voice transcription

Copy `.env.example` to `.env.local` and set the server-only credential:

```env
INTRON_API_KEY=your_real_api_key
```

Restart the development server after changing environment variables. Never place the key in client code, `public/`, screenshots, or a public repository. Without the key, the typed-question workflow remains available.

The backend sends short recordings to `https://infer.voice.intron.io/file/v1/upload/sync` and reads the documented `data.audio_transcript` response field. The initial language hint is English; Yoruba-English support should be validated with benchmark audio before making a language-performance claim.

## Scope

The first version covers basic agricultural education only. It does not diagnose crop disease, prescribe fertilizer quantities, forecast weather, or replace an agricultural extension officer.

## Benchmark

The benchmark is separate from the product. Copy `benchmark/manifest.example.json` to `benchmark/manifest.json` and replace it with a fixed, consented, de-identified audio subset. Do not commit private recordings or raw licensed datasets.

The runner compares Sahara/Intron, Whisper, and a third model using the same manifest and reports WER, CER, latency, and failures:

```bash
npm run benchmark
```

Set `WHISPER_COMMAND` and `THIRD_MODEL_COMMAND` in `.env.local` to commands that accept `{file}` and print one transcript to stdout. The runner records missing adapters as failures; it never invents scores. Use `benchmark/REPORT_TEMPLATE.md` for the three-page report structure.

### Recommended AfriSwitch alternative

If AfriSwitch approval is unavailable, use the original consented agricultural evaluation set described in `benchmark/CUSTOM_DATASET_PROTOCOL.md`. A smaller domain-specific set with transparent consent and transcript review is stronger for this product than an unrelated generic dataset. Package it with `benchmark/prepare_custom_subset.py`. Sahara, Whisper, and the third model must receive the same generated manifest and audio files. Do not use the synthetic fixture for benchmark results.
