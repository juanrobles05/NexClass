import os
import pickle
import numpy as np
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
import requests
import hashlib

# Load project .env (falls back to any .env) and configure Gemini API key
dotenv_path = find_dotenv('.env') or find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    # fallback: attempt to load .env in repo root
    load_dotenv('.env')

GEN_AI_KEY = os.getenv('GENERATIVE_AI_KEY') or os.getenv('GENAI_KEY')
if not GEN_AI_KEY:
    raise RuntimeError("Generative AI key not found. Set GENERATIVE_AI_KEY in your .env file.")

# Configure the Google Generative AI client
genai.configure(api_key=GEN_AI_KEY)


def _local_fallback_embedding(text: str, dim: int = 512):
    """Deterministic local fallback embedding.

    This is a cheap, dependency-free fallback that produces a fixed-size
    numeric vector based on token hashes. It's not semantically equivalent to
    Gemini embeddings but allows the app to continue operating when the remote
    embedding service is unavailable or configured incorrectly.
    """
    vec = np.zeros(dim, dtype=float)
    # Simple tokenization by whitespace
    for i, token in enumerate(text.split()):
        # Hash token to an integer and map into vector index
        h = int(hashlib.md5(token.encode('utf-8')).hexdigest()[:8], 16)
        idx = h % dim
        vec[idx] += 1.0
    # Normalize
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def generate_embedding(text: str):
    """Generate an embedding for the given text using Gemini (Google Generative AI).

    Tries SDK helper, falls back to REST; if REST returns 404 or another error,
    falls back to a deterministic local embedding so the application can continue.
    """
    model = "text-embedding-gecko-001"
    try:
        if hasattr(genai, 'embeddings'):
            response = genai.embeddings.create(
                model=model,
                input=text,
            )
            embedding = response.data[0].embedding
            return embedding
        else:
            raise AttributeError("genai.embeddings not available")
    except AttributeError:
        # Fallback to HTTP call
        try:
            api_key = GEN_AI_KEY
            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:embed?key={api_key}"
            payload = {"input": text}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            if 'data' in data and isinstance(data['data'], list) and 'embedding' in data['data'][0]:
                return data['data'][0]['embedding']
            if 'embedding' in data:
                return data['embedding']
            raise RuntimeError(f"Unexpected embedding response shape: {data}")
        except requests.HTTPError as http_err:
            status = http_err.response.status_code if http_err.response is not None else None
            # If model not found (404) or access problems, fallback locally and log
            print(f"HTTP error calling Gemini embeddings (status={status}): {http_err}")
            print("Falling back to local deterministic embedding. Check model name and API key or SDK version.")
            return _local_fallback_embedding(text)
        except Exception as e:
            print(f"Error generating embedding with Gemini (HTTP fallback): {e}")
            print("Falling back to local deterministic embedding.")
            return _local_fallback_embedding(text)
    except Exception as e:
        print(f"Error generating embedding with Gemini SDK: {e}")
        print("Falling back to local deterministic embedding.")
        return _local_fallback_embedding(text)


def save_embedding_to_binary(embedding):
    return pickle.dumps(embedding)


def load_embedding_from_binary(binary_embedding):
    return pickle.loads(binary_embedding)


def calcular_similitud(embedding_aspirante, embedding_empleo):
    dot_product = np.dot(embedding_aspirante, embedding_empleo)
    norm_aspirante = np.linalg.norm(embedding_aspirante)
    norm_empleo = np.linalg.norm(embedding_empleo)
    return dot_product / (norm_aspirante * norm_empleo)
