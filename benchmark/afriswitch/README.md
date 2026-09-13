---
license: cc-by-nc-sa-4.0
language:
- af
- am
- fr
- ha
- ig
- rw
- lg
- om
- pcm
- sn
- sw
- tn
- yo
- zu
- en
multilinguality:
- multilingual
- code-switching
task_categories:
- automatic-speech-recognition
pretty_name: AfriSwitch
size_categories:
- 10K<n<100K
tags:
- code-switching
- speech
- african-languages
- asr
configs:
- config_name: afrikaans
  data_files:
  - split: test
    path: data/afrikaans/test-*.parquet
- config_name: amharic
  data_files:
  - split: test
    path: data/amharic/test-*.parquet
- config_name: french
  data_files:
  - split: test
    path: data/french/test-*.parquet
- config_name: hausa
  data_files:
  - split: test
    path: data/hausa/test-*.parquet
- config_name: igbo
  data_files:
  - split: test
    path: data/igbo/test-*.parquet
- config_name: kinyarwanda
  data_files:
  - split: test
    path: data/kinyarwanda/test-*.parquet
- config_name: luganda
  data_files:
  - split: test
    path: data/luganda/test-*.parquet
- config_name: oromo
  data_files:
  - split: test
    path: data/oromo/test-*.parquet
- config_name: pidgin
  data_files:
  - split: test
    path: data/pidgin/test-*.parquet
- config_name: shona
  data_files:
  - split: test
    path: data/shona/test-*.parquet
- config_name: swahili
  data_files:
  - split: test
    path: data/swahili/test-*.parquet
- config_name: tswana
  data_files:
  - split: test
    path: data/tswana/test-*.parquet
- config_name: yoruba
  data_files:
  - split: test
    path: data/yoruba/test-*.parquet
- config_name: zulu
  data_files:
  - split: test
    path: data/zulu/test-*.parquet
---

# AfriSwitch: In-the-Wild African Code-Switched Speech Benchmark

## Dataset Description

AfriSwitch is a 54.41-hour, human-transcribed **test benchmark** of in-the-wild, conversational
code-switched speech spanning 14 African languages: **Amharic, Pidgin, Kinyarwanda, Yoruba, Hausa,
Oromo, Igbo, Zulu, French, Shona, Swahili, Tswana, Luganda, Afrikaans**, each switching with English.

This release is distributed as a single **`test`** split (evaluation-only benchmark).

- **License:** CC BY NC SA 4.0
- **Total duration:** 54.41 hours
- **Total utterances:** 16,602
- **Total code-switch events (S\*):** 73,486
- **Split:** `test` (only)

## Dataset Statistics

| Language | Hours | Utterances | Avg. Switch Points | Total S* | CMI |
|---|---|---|---|---|---|
| Kinyarwanda | 5.00 | 1,577 | 4.51 | 7,108 | 16.95 |
| Amharic | 5.00 | 1,229 | 4.60 | 5,650 | 13.11 |
| Zulu | 5.00 | 1,465 | 4.40 | 6,447 | 24.76 |
| Igbo | 5.00 | 1,848 | 4.10 | 7,575 | 27.64 |
| Yoruba | 5.00 | 1,877 | 5.33 | 10,002 | 22.93 |
| Hausa | 5.00 | 1,515 | 4.00 | 6,053 | 13.09 |
| Pidgin | 4.56 | 1,801 | 4.29 | 7,719 | 30.15 |
| Oromo | 4.25 | 1,217 | 2.95 | 3,586 | 13.39 |
| Swahili | 3.89 | 650 | 8.84 | 5,748 | 23.23 |
| Shona | 3.86 | 1,155 | 4.85 | 5,599 | 24.55 |
| French | 3.22 | 903 | 3.00 | 2,713 | 10.92 |
| Tswana | 2.74 | 805 | 4.38 | 3,529 | 23.22 |
| Luganda | 1.21 | 362 | 3.97 | 1,437 | 25.64 |
| Afrikaans | 0.68 | 198 | 1.62 | 320 | 5.52 |
| **Total** | **54.41** | **16,602** | **4.43** | **73,486** | **20.84** |

**Switch points (S\*)** count alternation points where a token's language tag differs from the
preceding token's (Gamb&auml;ck and Das, 2016). **Code-Mixing Index (CMI)** follows Das and Gamb&auml;ck
(2014): 0 = monolingual, higher = more balanced mixing.

## Dataset Structure

Each example includes:

- `audio`: the speech segment, 16 kHz HuggingFace Audio feature (`bytes` + `path`)
- `language`: primary/matrix language of the utterance
- `filename`: audio clip filename
- `transcription`: verbatim human transcription (plain text)
- `transcription_tagged`: same transcription with English spans wrapped in `[[EN]]`…`[[/EN]]`
- `cmi`: per-utterance Code-Mixing Index
- `num_switch_points`: per-utterance language-alternation count
- `duration`: utterance length in seconds

Each language is a separate config (subset), selectable in the dataset viewer, each with a single
`test` split. Load e.g. `load_dataset("intronhealth/AfriSwitch", "hausa", split="test")`.

## Dataset Creation

Audio was sourced from publicly available YouTube videos and podcasts under permissive licenses;
bilingual annotators selected material for the presence of code-switching and produced verbatim
transcriptions. For this release the data was processed in two steps:

1. **Character-rate filtered** &mdash; utterances outside each language's 5th&ndash;95th percentile of
   characters-per-second (misaligned audio/text) were removed.
2. **Code-mixing metrics added** &mdash; per-utterance **CMI** and **switch points** were computed
   for each utterance.

The released dataset contains transcriptions and processed audio segments only, with no links back to
original source media. No annotator demographic information is included.

## Licensing Information

Released under **Attribution-NonCommercial-ShareAlike 4.0 (CC BY NC SA 4.0)**.
