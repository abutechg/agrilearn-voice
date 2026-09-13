import { exec } from "node:child_process";
import { promises as fs } from "node:fs";
import { performance } from "node:perf_hooks";
import { promisify } from "node:util";
import path from "node:path";

const execAsync = promisify(exec);
const root = process.cwd();
const manifestPath = process.argv[2] || "benchmark/manifest.json";
const outputPath = process.argv[3] || "benchmark/results.json";
const endpoint = process.env.SAHARA_ENDPOINT || "https://infer.voice.intron.io/file/v1/upload/sync";

function normalize(text) {
  return String(text || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^\p{L}\p{N}\s]/gu, " ").replace(/\s+/g, " ").trim();
}
function tokens(text) { return normalize(text).split(" ").filter(Boolean); }
function editDistance(a, b) {
  const previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let row = 1; row <= a.length; row += 1) {
    const current = [row];
    for (let column = 1; column <= b.length; column += 1) current[column] = Math.min(current[column - 1] + 1, previous[column] + 1, previous[column - 1] + (a[row - 1] === b[column - 1] ? 0 : 1));
    for (let column = 0; column <= b.length; column += 1) previous[column] = current[column];
  }
  return previous[b.length];
}
function rate(reference, hypothesis, unit) {
  const expected = unit === "word" ? tokens(reference) : [...normalize(reference).replace(/\s/g, "")];
  const actual = unit === "word" ? tokens(hypothesis) : [...normalize(hypothesis).replace(/\s/g, "")];
  return expected.length ? editDistance(expected, actual) / expected.length : (actual.length ? 1 : 0);
}
async function transcribeSahara(item) {
  if (!process.env.INTRON_API_KEY) throw new Error("INTRON_API_KEY is not configured");
  const buffer = await fs.readFile(path.resolve(root, item.audio));
  const body = new FormData();
  body.append("audio_file_name", path.basename(item.audio));
  body.append("audio_file_blob", new Blob([buffer], { type: "audio/wav" }), path.basename(item.audio));
  body.append("use_language_asr_input", process.env.SAHARA_LANGUAGE || "en");
  const response = await fetch(endpoint, { method: "POST", headers: { Authorization: `Bearer ${process.env.INTRON_API_KEY}` }, body });
  const result = await response.json();
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const transcript = result?.data?.audio_transcript || result?.transcript || result?.text || "";
  if (!transcript) throw new Error("No transcript returned");
  return transcript;
}
async function transcribeCommand(item, variableName) {
  const template = process.env[variableName];
  if (!template) throw new Error(`${variableName} is not configured`);
  const command = template.replaceAll("{file}", JSON.stringify(path.resolve(root, item.audio)));
  const { stdout } = await execAsync(command, { cwd: root, windowsHide: true, maxBuffer: 1024 * 1024 });
  const transcript = stdout.trim();
  if (!transcript) throw new Error(`${variableName} returned no transcript on stdout`);
  return transcript;
}
const models = [
  { id: "sahara", label: "Sahara/Intron", run: transcribeSahara },
  { id: "whisper", label: "Whisper", run: (item) => transcribeCommand(item, "WHISPER_COMMAND") },
  { id: "third", label: "Third model", run: (item) => transcribeCommand(item, "THIRD_MODEL_COMMAND") },
];
const manifest = JSON.parse(await fs.readFile(path.resolve(root, manifestPath), "utf8"));
if (!Array.isArray(manifest) || !manifest.length) throw new Error("Manifest must contain at least one sample");
const result = { generatedAt: new Date().toISOString(), manifest: manifestPath, models: {} };
for (const model of models) {
  const samples = [];
  for (const item of manifest) {
    const started = performance.now();
    try {
      const transcript = await model.run(item);
      samples.push({ id: item.id, reference: item.reference, transcript, languagePair: item.languagePair, topic: item.topic, wer: rate(item.reference, transcript, "word"), cer: rate(item.reference, transcript, "char"), latencyMs: Math.round(performance.now() - started) });
    } catch (error) {
      samples.push({ id: item.id, reference: item.reference, error: error.message, latencyMs: Math.round(performance.now() - started) });
    }
  }
  const successful = samples.filter((sample) => !sample.error);
  result.models[model.id] = { label: model.label, samples, summary: { total: samples.length, successful: successful.length, failures: samples.length - successful.length, wer: successful.length ? successful.reduce((sum, sample) => sum + sample.wer, 0) / successful.length : null, cer: successful.length ? successful.reduce((sum, sample) => sum + sample.cer, 0) / successful.length : null, meanLatencyMs: successful.length ? successful.reduce((sum, sample) => sum + sample.latencyMs, 0) / successful.length : null } };
}
await fs.mkdir(path.dirname(path.resolve(root, outputPath)), { recursive: true });
await fs.writeFile(path.resolve(root, outputPath), `${JSON.stringify(result, null, 2)}\n`);
console.log(`Wrote ${outputPath}. Missing model commands are recorded as failures; no scores were fabricated.`);
