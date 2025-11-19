from fastapi import FastAPI
from fuzzywuzzy import process
import re

app = FastAPI()

# Dataset menu
menu_dataset = [
    "Pempek Adaan",
    "Pempek Lenjer",
    "Pempek Kapal Selam",
    "Pempek Keriting",
    "Pempek Kulit"
]

# Threshold kemiripan minimal untuk fuzzy matching
MATCH_THRESHOLD = 60

def normalize(text: str) -> str:
    """
    Bersihkan teks untuk pencarian:
    - Lowercase
    - Hapus karakter non-alphanumeric
    - Hapus spasi ekstra
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Buat versi normalisasi dari dataset
normalized_dataset = {normalize(menu): menu for menu in menu_dataset}

@app.get("/")
def root():
    return {"message": "API Menu Recommender aktif"}

@app.get("/recommend")
def recommend(menu_name: str):
    """
    Hybrid search:
    1. Cari exact match (case-insensitive + ignore spaces/punctuation)
    2. Jika tidak ada, gunakan fuzzy matching untuk saran menu terdekat
    """
    normalized_query = normalize(menu_name)

    # Exact match
    if normalized_query in normalized_dataset:
        return {"menu_found": normalized_dataset[normalized_query]}

    # Fuzzy matching
    match = process.extractOne(normalized_query, list(normalized_dataset.keys()))
    if match and match[1] >= MATCH_THRESHOLD:
        return {
            "menu_not_found": menu_name,
            "suggested_menu": normalized_dataset[match[0]],
            "similarity_score": match[1]
        }

    # Tidak ada yang cocok
    return {
        "error": f"Menu '{menu_name}' tidak ditemukan dalam dataset",
        "note": "Coba periksa penulisan menu atau gunakan nama lain"
    }
