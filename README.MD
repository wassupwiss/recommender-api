# Kuliner Palembang Recommendation API

API rekomendasi kuliner Palembang menggunakan FastAPI dengan sistem rekomendasi berbasis Content-Based Filtering menggunakan TF-IDF dan Cosine Similarity.

## 📋 Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Joblib
- Scikit-learn
- Pandas
- Python-Levenshtein

## 🚀 Installation

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Server akan berjalan di `http://localhost:7860`

### Docker Setup

```bash
# Build Docker image
docker build -t kuliner-recommendation .

# Run container
docker run -p 7860:7860 kuliner-recommendation
```

## 📚 API Documentation

### Base URL
```
http://localhost:7860
```

---

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Mengecek status API

**Request:** Tidak ada parameter

**Response:**
```json
{
  "message": "Hello! Welcome to Kuliner Palembang Recommendation API"
}
```

**Example:**
```bash
curl http://localhost:7860/
```

---

### 2. Get Recommendations

**Endpoint:** `POST /recommend`

**Description:** Mendapatkan rekomendasi kuliner berdasarkan input nama kuliner

**Request Body:**
```json
{
  "kuliner": "string",
  "num_recommendations": 10
}
```

**Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `kuliner` | string | ✅ Yes | - | Nama kuliner yang menjadi acuan rekomendasi |
| `num_recommendations` | integer | ❌ No | 10 | Jumlah rekomendasi yang diinginkan |

**Success Response (200):**
```json
{
  "kuliner_input": "Model",
  "recommendations": [
    {
      "nama_kuliner": "Pempek Adaan",
      "similarity_score": 0.8542
    },
    {
      "nama_kuliner": "Tekwan",
      "similarity_score": 0.7834
    },
    {
      "nama_kuliner": "Celimpungan",
      "similarity_score": 0.7521
    }
  ]
}
```

**Error Response (404):**
```json
{
  "detail": "Kuliner dengan nama 'Nasi Goreng' tidak ditemukan dalam dataset."
}
```

**Error Response (503):**
```json
{
  "detail": "Models not loaded. Please check server logs."
}
```

---

## 🧪 Testing Examples

### cURL

```bash
# Basic request
curl -X POST "http://localhost:7860/recommend" \
  -H "Content-Type: application/json" \
  -d '{"kuliner": "Model", "num_recommendations": 5}'

# With more recommendations
curl -X POST "http://localhost:7860/recommend" \
  -H "Content-Type: application/json" \
  -d '{"kuliner": "Pempek Adaan", "num_recommendations": 10}'
```

### Python

```python
import requests

# Basic request
response = requests.post(
    "http://localhost:7860/recommend",
    json={
        "kuliner": "Model",
        "num_recommendations": 5
    }
)

print(response.json())

# Handle response
if response.status_code == 200:
    data = response.json()
    print(f"Input: {data['kuliner_input']}")
    for i, rec in enumerate(data['recommendations'], 1):
        print(f"{i}. {rec['nama_kuliner']} (Score: {rec['similarity_score']:.4f})")
elif response.status_code == 404:
    print("Kuliner tidak ditemukan")
elif response.status_code == 503:
    print("Server error: Models not loaded")
```

### JavaScript/Fetch

```javascript
// Basic request
fetch('http://localhost:7860/recommend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        kuliner: 'Model',
        num_recommendations: 5
    })
})
.then(response => response.json())
.then(data => {
    console.log('Input:', data.kuliner_input);
    data.recommendations.forEach((rec, i) => {
        console.log(`${i+1}. ${rec.nama_kuliner} (Score: ${rec.similarity_score})`);
    });
})
.catch(error => console.error('Error:', error));
```

### HTTPie

```bash
# Install httpie: pip install httpie

http POST http://localhost:7860/recommend \
  kuliner="Model" \
  num_recommendations:=5
```

### Postman

1. Method: `POST`
2. URL: `http://localhost:7860/recommend`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "kuliner": "Model",
  "num_recommendations": 5
}
```

---

## 🔧 Project Structure

```
backend-recommendation-xplorin/
├── app.py                 # Main FastAPI application
├── main.py               # Utility functions (unused in production)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── README.MD            # Documentation
└── models/              # Pre-trained models
    ├── cosine_sim.pkl
    ├── data.pkl
    ├── indices.pkl
    ├── tfidf_matrix.pkl
    └── tfidf_vectorizer.pkl
```

---

## 🌐 Deploy to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Select **Docker** as SDK
3. Push the following files:
   - `Dockerfile`
   - `app.py`
   - `requirements.txt`
   - `models/` folder

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
# Copy all files
git add .
git commit -m "Initial deployment"
git push
```

---

## 📊 API Response Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Rekomendasi berhasil didapatkan |
| 404 | Not Found - Kuliner tidak ditemukan dalam dataset |
| 422 | Validation Error - Request body tidak valid |
| 503 | Service Unavailable - Models gagal dimuat |

---

## 🛠️ Development

### Interactive API Documentation

Setelah menjalankan server, akses dokumentasi interaktif di:
- Swagger UI: `http://localhost:7860/docs`
- ReDoc: `http://localhost:7860/redoc`

### Model Files

Model files harus berada di folder `models/` dengan struktur:
- `tfidf_vectorizer.pkl` - TF-IDF Vectorizer
- `tfidf_matrix.pkl` - TF-IDF Matrix
- `cosine_sim.pkl` - Cosine Similarity Matrix
- `data.pkl` - Dataset DataFrame
- `indices.pkl` - Index mapping

---

## 📝 License

MIT License

---

## 👥 Contributors

- wassupwiss

---

## 📧 Contact

For issues and questions, please open an issue on GitHub.
