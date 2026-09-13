export async function POST(request) {
  try {
    const formData = await request.formData();
    const audio = formData.get("audio");
    if (!audio || typeof audio === "string") return Response.json({ error: "No audio provided." }, { status: 400 });
    if (audio.size > 15 * 1024 * 1024) return Response.json({ error: "Audio file is too large." }, { status: 400 });
    if (!process.env.INTRON_API_KEY) return Response.json({ error: "Sahara is not configured yet. You can type your question instead." }, { status: 503 });

    const language = formData.get("language") || "yo";
    const body = new FormData();
    body.append("audio_file_name", audio.name || "recording.webm");
    body.append("audio_file_blob", audio);
    body.append("use_language_asr_input", language);
    const response = await fetch("https://infer.voice.intron.io/file/v1/upload/sync", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.INTRON_API_KEY}` },
      body,
    });
    const result = await response.json();
    if (!response.ok) return Response.json({ error: "Sahara could not transcribe this recording." }, { status: response.status });
    let transcript = result?.data?.audio_transcript || result?.transcript || result?.text || result?.data?.transcript || result?.data?.text;
    const fileId = result?.data?.file_id;

    // If Intron queued the file for async processing, poll the status endpoint until ready
    if ((!transcript || !transcript.trim()) && fileId) {
      for (let attempt = 0; attempt < 8; attempt++) {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        try {
          const pollResponse = await fetch(`https://infer.voice.intron.io/file/v1/status/${fileId}`, {
            headers: { Authorization: `Bearer ${process.env.INTRON_API_KEY}` },
          });
          if (pollResponse.ok) {
            const pollResult = await pollResponse.json();
            const polledTranscript = pollResult?.data?.audio_transcript || pollResult?.transcript || pollResult?.data?.transcript;
            if (polledTranscript && polledTranscript.trim()) {
              transcript = polledTranscript;
              break;
            }
          }
        } catch {}
      }
    }

    if (!transcript || !transcript.trim()) {
      return Response.json({ error: "Sahara returned no transcript. Try speaking for a little longer or a clearer recording." }, { status: 502 });
    }

    return Response.json({ transcript, status: "COMPLETED", fileId: fileId || null });
  } catch {
    return Response.json({ error: "The transcription service is unavailable. Try typing your question." }, { status: 500 });
  }
}