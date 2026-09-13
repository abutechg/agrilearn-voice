"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import agriculture from "@/benchmark/agriculture_answer_bank.json";
import { findAnswer } from "@/lib/questionMatcher";

const demoQuestions = agriculture.slice(0, 3).map((entry) => entry.question);

function MicIcon() {
  return <svg aria-hidden="true" viewBox="0 0 24 24" className="mic-icon"><path d="M12 14.5a3.5 3.5 0 0 0 3.5-3.5V6a3.5 3.5 0 1 0-7 0v5a3.5 3.5 0 0 0 3.5 3.5Z" /><path d="M5.5 10.5a6.5 6.5 0 0 0 13 0M12 17v4M8.5 21h7" /></svg>;
}

function Waveform({ active }) {
  return <div className={`waveform ${active ? "is-active" : ""}`} aria-hidden="true">{[18, 30, 44, 26, 38, 22, 48, 30, 40, 20, 34, 25].map((height, index) => <span key={index} style={{ "--bar-height": `${height}%` }} />)}</div>;
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [transcript, setTranscript] = useState("");
  const [answer, setAnswer] = useState(null);
  const [recording, setRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("yo");
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const recordingTimer = useRef(null);
  useEffect(() => () => mediaRecorder.current?.stream?.getTracks().forEach((track) => track.stop()), []);
  useEffect(() => () => clearInterval(recordingTimer.current), []);
  function resolveQuestion(value) { const result = findAnswer(value, agriculture); setQuestion(value); setTranscript(value); setAnswer(result); setError(""); }
  function startRecording() {
    if (!navigator.mediaDevices?.getUserMedia) { setError("Microphone recording is not available here. You can type your question instead."); return; }
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      const mimeType = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"].find((type) => MediaRecorder.isTypeSupported(type));
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined); audioChunks.current = [];
      recorder.ondataavailable = (event) => { if (event.data && event.data.size > 0) audioChunks.current.push(event.data); };
      recorder.onstop = () => {
        if (audioChunks.current.length > 0) {
          transcribe(new Blob(audioChunks.current, { type: recorder.mimeType || "audio/webm" }));
        } else {
          setError("No audio was recorded. Please speak into the microphone and try again.");
        }
      };
      recorder.start(250); mediaRecorder.current = recorder; setRecording(true); setRecordingSeconds(0); setError("");
      recordingTimer.current = setInterval(() => setRecordingSeconds((seconds) => seconds + 1), 1000);
      setTimeout(() => { if (mediaRecorder.current === recorder && recorder.state === "recording") stopRecording(); }, 30000);
    }).catch(() => setError("Microphone access was not granted. You can type your question instead."));
  }
  function stopRecording() { clearInterval(recordingTimer.current); if (mediaRecorder.current?.state === "recording") mediaRecorder.current.stop(); mediaRecorder.current?.stream.getTracks().forEach((track) => track.stop()); setRecording(false); }
  async function transcribe(audio) {
    setLoading(true); setError("");
    try {
      const formData = new FormData();
      formData.append("audio", audio, audio.name || "recording.webm");
      formData.append("language", selectedLanguage);
      const response = await fetch("/api/transcribe", { method: "POST", body: formData });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Transcription failed.");
      if (!result.transcript?.trim()) throw new Error("Sahara returned no transcript. Try speaking a bit longer and more clearly.");
      resolveQuestion(result.transcript);
    }
    catch (transcriptionError) { setError(transcriptionError.message || "We could not transcribe that recording. Try typing your question."); } finally { setLoading(false); }
  }
  function selectAudio(event) { setAudioFile(event.target.files?.[0] || null); setError(""); }
  function transcribeSelectedAudio() { if (!audioFile) { setError("Choose a short audio recording first."); return; } transcribe(audioFile); }
  function submitQuestion(event) { event.preventDefault(); if (question.trim()) resolveQuestion(question.trim()); }
  return <main className="app-shell">
    <header className="topbar">
      <Link className="brand" href="/" aria-label="AgriLearn Voice home"><span className="brand-mark">A</span><span>AgriLearn <em>Voice</em></span></Link>
      <div className="language-pill">
        <span className="status-dot" />
        <select
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          aria-label="Select ASR Language"
          style={{ background: 'transparent', border: 'none', color: 'inherit', font: 'inherit', cursor: 'pointer', outline: 'none' }}
        >
          <option value="yo" style={{ background: '#fbfaf5', color: '#17372d' }}>Yoruba + English</option>
          <option value="sw" style={{ background: '#fbfaf5', color: '#17372d' }}>Swahili + English</option>
          <option value="ha" style={{ background: '#fbfaf5', color: '#17372d' }}>Hausa + English</option>
          <option value="fr" style={{ background: '#fbfaf5', color: '#17372d' }}>French</option>
          <option value="ar" style={{ background: '#fbfaf5', color: '#17372d' }}>Arabic</option>
          <option value="en" style={{ background: '#fbfaf5', color: '#17372d' }}>English</option>
        </select>
      </div>
    </header>
    <section className="hero-grid"><div className="intro-block"><p className="eyebrow">FIELD NOTES / 01</p><h1>Ask the land.<br /><span>Learn by voice.</span></h1><p className="intro-copy">Short, clear agricultural lessons for the moments when typing gets in the way.</p><div className="trust-row"><span className="leaf-symbol">+</span><span>Curated learning, not guesswork</span></div></div>
      <div className="question-panel"><div className="panel-heading"><span>YOUR QUESTION</span><span className="panel-index">01 / 01</span></div><div className="recording-stage"><Waveform active={recording || loading} /><button className={`record-button ${recording ? "is-recording" : ""}`} onClick={recording ? stopRecording : startRecording} aria-label={recording ? "Stop recording" : "Start recording"} disabled={loading}><MicIcon /></button><p className="recording-label">{loading ? "Transcribing your question..." : recording ? `Recording ${recordingSeconds}s - tap to finish` : "Tap to start speaking"}</p><p className="recording-hint">Speak clearly for 2–10 seconds, then tap again to finish</p></div><div className="file-row"><label className="file-picker"><span>{audioFile ? audioFile.name : "Choose an audio file"}</span><input type="file" accept="audio/*" onChange={selectAudio} /></label><button type="button" className="transcribe-button" onClick={transcribeSelectedAudio} disabled={loading}>{loading ? "Transcribing..." : "Transcribe question"}</button></div><form className="text-form" onSubmit={submitQuestion}><input aria-label="Type your agricultural question" value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="e.g. What is crop rotation?" /><button type="submit" className="send-button" aria-label="Ask question">Ask <span>↗</span></button></form>{error && <p className="error-message" role="alert">{error}</p>}</div>
    </section>
    <section className="content-grid"><div className="examples-block"><div className="section-label"><span>TRY A LESSON</span><span className="rule" /></div><div className="example-list">{demoQuestions.map((demoQuestion, index) => <button key={demoQuestion} className="example-button" onClick={() => resolveQuestion(demoQuestion)}><span>0{index + 1}</span>{demoQuestion}<b>↗</b></button>)}</div></div><div className="answer-block"><div className="section-label"><span>LESSON RESPONSE</span><span className="topic-label">{answer?.topic || "READY WHEN YOU ARE"}</span></div><div className={`answer-card ${answer ? "has-answer" : ""}`}>{answer ? <><p className={`answer-confidence ${answer.matched ? "is-matched" : "is-uncertain"}`}>{answer.matched ? "CURATED TOPIC MATCH" : "OUTSIDE CURRENT KNOWLEDGE BASE"}</p><p className="answer-kicker">{transcript}</p><p className="answer-text">{answer.answer}</p>{answer.safetyNote && <p className="safety-note">{answer.safetyNote}</p>}<button className="listen-button" onClick={() => window.speechSynthesis?.speak(new SpeechSynthesisUtterance(answer.answer))}><span>◖</span> Listen to lesson</button></> : <><div className="empty-sprout">+</div><p className="empty-title">Your lesson will appear here.</p><p className="empty-copy">Ask a question by voice or choose one of the examples.</p></>}</div></div></section>
    <footer className="footer"><span>AGRILEARN / MULTILINGUAL (YORUBA, SWAHILI, HAUSA, FRENCH, ARABIC, ENGLISH)</span><span>Built for clearer learning in the field</span></footer>
  </main>;
}
