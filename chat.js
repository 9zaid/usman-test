// Chat backend for the web widget.
// Test fixture for the Cytex AI-BOM scanner: every risky pattern is deliberate.
import express from "express";
import OpenAI from "openai";
import { exec } from "child_process";

const app = express();
app.use(express.json());

// Hardcoded AI API key (cytex-ai.js.hardcoded-ai-api-key, gitleaks).
const openai = new OpenAI({ apiKey: "iOaZNLliMjy3nIolkVAI0p1hougRRTmstyGhlUN8pkfoXSol" });

app.post("/api/chat", async (req, res) => {
  // Request body into the prompt (cytex-ai.js.prompt-injection.user-input-to-llm).
  const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: req.body.messages,
  });
  res.json({ answer: completion.choices[0].message.content });
});

app.post("/api/run", async (req, res) => {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "One shell command for: " + req.body.task }],
  });
  // LLM output executed (cytex-ai.js.llm-output-to-dangerous-sink).
  exec(completion.choices[0].message.content, (err, stdout) => res.send(stdout));
});

app.post("/api/formula", async (req, res) => {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "JavaScript expression for: " + req.body.formula }],
  });
  res.json({ value: eval(completion.choices[0].message.content) });
});

app.listen(3000);
