from fastapi import FastAPI
from models import TrackInput
from track_utils import calculate_similarity_score

app = FastAPI()

@app.post("/compare")
async def compare(data: TrackInput):
    score, distance, user_path = calculate_similarity_score(
        data.user_path,
        data.ground_truth,
        num_points=100,
    )
    return {
        "score": score,
        "distance": distance,
        "metric": "interpolate→normalize→circular-shift",
        "user_path": user_path.tolist(), 
    }