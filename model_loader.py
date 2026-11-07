"""Loads the sentiment and summarisation models.

Test fixture for the Cytex AI-BOM scanner: unsafe model loading on purpose.
"""
import pickle

import joblib
import requests
import torch
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

MODEL_URL = "https://models.example.invalid/sentiment_classifier.pkl"


def load_summarizer():
    # Remote code from the hub without a pinned revision (cytex-ai.py.trust-remote-code).
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    return tokenizer, model


def load_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def load_checkpoint():
    # torch.load without weights_only (cytex-ai.py.torch-load-unsafe) on a hub
    # download (cytex-ai.py.untrusted-model-deserialization).
    path = hf_hub_download(repo_id="acme/reranker", filename="reranker.pt")
    return torch.load(path)


def load_remote_classifier():
    # Pickle from a URL (cytex-ai.py.untrusted-model-deserialization).
    blob = requests.get(MODEL_URL, timeout=30).content
    return pickle.loads(blob)


def load_local_classifier():
    # The repo's own models/sentiment_classifier.pkl is what ModelScan flags.
    return joblib.load("models/sentiment_classifier.pkl")
