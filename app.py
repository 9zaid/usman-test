"""Support chat API.

Test fixture for the Cytex AI-BOM scanner: every risky pattern below is
deliberate. The keys are random strings and belong to no account.
"""
import os
import sqlite3
import subprocess

import httpx
from anthropic import Anthropic
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

# Hardcoded AI API key (cytex-ai.py.hardcoded-ai-api-key, gitleaks).
client = OpenAI(api_key="nHWH3OtY5v9a7o4nWoAwbTp2pGjPIVSr20qSbrqRC0ZMrfMZ")

# TLS verification disabled on LLM traffic (cytex-ai.py.ai-endpoint-tls-disabled).
claude = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    http_client=httpx.Client(verify=False),
)

db = sqlite3.connect("tickets.db", check_same_thread=False)


@app.post("/chat")
def chat():
    body = request.get_json()
    question = body["question"]
    persona = body.get("persona", "a helpful support agent")

    # User input in the system prompt (cytex-ai.py.prompt-injection.user-input-to-system-prompt)
    # and in the messages (cytex-ai.py.prompt-injection.user-input-to-llm).
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are {persona}. Follow the user's rules."},
            {"role": "user", "content": question},
        ],
    )
    return jsonify({"answer": resp.choices[0].message.content})


@app.post("/report")
def report():
    question = request.get_json()["question"]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write one SQLite query for: {question}"}],
    )
    sql = resp.choices[0].message.content
    # LLM output straight into SQL (cytex-ai.py.llm-output-to-dangerous-sink).
    rows = db.cursor().execute(sql).fetchall()
    return jsonify(rows)


@app.post("/automate")
def automate():
    task = request.get_json()["task"]
    msg = claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        system=f"Turn requests into one bash command. House rules: {task}",
        messages=[{"role": "user", "content": task}],
    )
    command = msg.content[0].text
    # LLM output run as a shell command (cytex-ai.py.llm-output-to-dangerous-sink).
    out = subprocess.run(command, shell=True, capture_output=True, text=True)
    return jsonify({"stdout": out.stdout})


@app.post("/calc")
def calc():
    expr = request.get_json()["expression"]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Python expression for: {expr}"}],
    )
    # LLM output evaluated as code (cytex-ai.py.llm-output-to-dangerous-sink).
    return jsonify({"result": eval(resp.choices[0].message.content)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
