from pydantic import BaseModel
from typing import List

class TrackInput(BaseModel):
    user_path: List[List[float]]
    ground_truth: List[List[float]]
