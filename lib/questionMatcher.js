export function normalizeText(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function findAnswer(text, entries) {
  const normalizedTranscript = normalizeText(text);
  let bestMatch = null;
  let bestScore = 0;

  for (const entry of entries) {
    let score = 0;
    const keywords = entry.keywords || [entry.question];
    for (const keyword of keywords) {
      const normalizedKeyword = normalizeText(keyword);
      if (normalizedTranscript.includes(normalizedKeyword)) score += normalizedKeyword.split(" ").length;
    }
    if (score > bestScore) { bestScore = score; bestMatch = entry; }
  }

  if (!bestMatch || bestScore === 0) return {
    matched: false,
    topic: "Try another topic",
    answer: "I could not confidently match that question to my agricultural knowledge base. Please try asking about soil preparation, maize planting, or weed management.",
  };

  return {
    matched: true,
    topic: bestMatch.topic || bestMatch.question,
    answer: bestMatch.answer,
    yorubaEnglishAnswer: bestMatch.yorubaEnglishAnswer,
    safetyNote: bestMatch.safetyNote,
  };
}