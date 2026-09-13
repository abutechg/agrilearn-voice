# AgriLearn Voice ASR Benchmark

**Status:** Draft. Replace every placeholder with measured results before submission.

## Objective
Compare Sahara/Intron, Whisper, and a third ASR model on the same consented, de-identified agricultural speech samples.

## Dataset
- Source/license: [record source and license]
- Languages/code-switching: [language pairs]
- Sample count and duration: [measured values]
- Split: [fixed evaluation split]
- Consent/privacy: [consent and de-identification process]

## Method
All models receive the same audio files. References are human-reviewed transcripts. Report normalization rules, model versions, language settings, hardware/API region, and whether network latency is included.

## Results

| Model | Samples | WER | CER | Mean latency (ms) | Failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sahara/Intron | [ ] | [ ] | [ ] | [ ] | [ ] |
| Whisper | [ ] | [ ] | [ ] | [ ] | [ ] |
| Third model | [ ] | [ ] | [ ] | [ ] | [ ] |

Do not fill this table with invented numbers. Copy measured values from `benchmark/results.json`.

## Error analysis
Describe code-switching substitutions, named entities, Yoruba words, noise, clipped audio, and model/API failures. Include representative examples without publishing private audio or identifying speaker metadata.

## Conclusion and limitations
Select the best model for the narrow AgriLearn Voice workflow based on measured error, latency, availability, and language coverage. Do not generalize beyond this evaluation set.
