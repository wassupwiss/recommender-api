from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import joblib
import os

app = FastAPI()

# Define paths for models
output_dir = 'models'

def load_recommendation_models(output_directory=output_dir):
    """
    Loads all recommendation system components from disk.
    """
    try:
        loaded_tfidf_vectorizer = joblib.load(os.path.join(output_directory, "tfidf_vectorizer.pkl"))
        loaded_tfidf_matrix = joblib.load(os.path.join(output_directory, "tfidf_matrix.pkl"))
        loaded_cosine_sim = joblib.load(os.path.join(output_directory, "cosine_sim.pkl"))
        loaded_df = joblib.load(os.path.join(output_directory, "data.pkl"))
        loaded_indices = joblib.load(os.path.join(output_directory, "indices.pkl"))
        print(f"All models and data successfully loaded from '{output_directory}'!")
        return loaded_tfidf_vectorizer, loaded_tfidf_matrix, loaded_cosine_sim, loaded_df, loaded_indices
    except FileNotFoundError as e:
        print(f"Error: One or more model files not found in '{output_directory}': {e}")
        return None, None, None, None, None

# Load models saat startup
print("Loading recommendation models...")
loaded_tfidf_vectorizer, loaded_tfidf_matrix, loaded_cosine_sim, loaded_df, loaded_indices = load_recommendation_models()

if loaded_cosine_sim is None or loaded_indices is None or loaded_df is None:
    print("Warning: Failed to load models. Recommendation endpoint will not work properly.")

class RecommendationRequest(BaseModel):
    kuliner: str
    num_recommendations: int = 10

class RecommendationResponse(BaseModel):
    kuliner_input: str
    recommendations: list

@app.get("/")
def root():
    return {"message": "Hello! Welcome to Kuliner Palembang Recommendation API"}

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    """
    Endpoint untuk mendapatkan rekomendasi kuliner berdasarkan input kuliner.
    """
    if loaded_cosine_sim is None or loaded_indices is None or loaded_df is None:
        raise HTTPException(status_code=503, detail="Models not loaded. Please check server logs.")
    
    kuliner = request.kuliner
    num_recommendations = request.num_recommendations
    
    # Check if kuliner exists in the dataset
    if kuliner not in loaded_indices:
        raise HTTPException(
            status_code=404, 
            detail=f"Kuliner dengan nama '{kuliner}' tidak ditemukan dalam dataset."
        )
    
    # Get recommendations
    idx = loaded_indices[kuliner]
    skor_kesamaan = list(enumerate(loaded_cosine_sim[idx]))
    skor_kesamaan = sorted(skor_kesamaan, key=lambda x: x[1], reverse=True)
    skor_kesamaan = skor_kesamaan[1:num_recommendations+1]
    
    # Build response with recommendations and similarity scores
    recommendations = []
    for i, score in skor_kesamaan:
        kuliner_name = loaded_df['Nama kuliner palembang'].iloc[i]
        recommendations.append({
            "nama_kuliner": kuliner_name,
            "similarity_score": float(score)
        })
    
    return RecommendationResponse(
        kuliner_input=kuliner,
        recommendations=recommendations
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)