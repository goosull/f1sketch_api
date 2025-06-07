import json
import sys
from track_utils import calculate_similarity_score, visualize_paths

def load_path(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    if len(sys.argv) != 3:
        print("사용법: python run_local.py user.json ground_truth.json")
        return

    user_path = load_path(sys.argv[1])
    ground_truth = load_path(sys.argv[2])

    score, distance = calculate_similarity_score(user_path, ground_truth)
    visualize_paths(user_path, ground_truth)
    print(f"\n✅ 유사도 점수: {score}/100")
    print(f"거리: {distance}\n")

if __name__ == "__main__":
    main()
