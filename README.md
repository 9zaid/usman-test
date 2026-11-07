# ai-scan-demo

A deliberately insecure AI app, used to exercise the Cytex AI-BOM devops
scanner. **Do not deploy it.** Every key is a random string that belongs to no
account, and every URL is under `.example.invalid`.

| File | What the scanner should find |
|---|---|
| `app.py` | OpenAI / Anthropic clients, models; prompt injection (system + messages), LLM output into SQL / shell / `eval`, hardcoded key, TLS disabled |
| `model_loader.py` | transformers / hub models; `trust_remote_code`, unsafe `torch.load`, pickle from a URL |
| `agent.py` | LangChain / LangGraph / CrewAI agents; shell-exec tool, built-in `ShellTool` |
| `mcp_server.py` | MCP server with shell / file / service tools |
| `web/chat.js` | OpenAI JS client; prompt injection, output into `exec` / `eval`, hardcoded key |
| `.env` | AI provider keys (gitleaks / trufflehog) |
| `models/sentiment_classifier.pkl` | unsafe pickle (ModelScan, critical) |
| `.claude/skills/release-helper/` | an agent skill with unsafe instructions (skill scanner) |
| `requirements.txt`, `package.json` | old package versions with known CVEs (Grype) |
