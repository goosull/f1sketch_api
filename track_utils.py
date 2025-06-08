# track_utils.py

import numpy as np

def interpolate_path(path: np.ndarray, num_points: int = 100) -> np.ndarray:
    path = np.array(path)
    if len(path) == num_points:
        return path
    deltas = np.diff(path, axis=0)
    dist   = np.insert(np.cumsum(np.linalg.norm(deltas, axis=1)), 0, 0)
    u_dist = np.linspace(0, dist[-1], num_points)
    x = np.interp(u_dist, dist, path[:,0])
    y = np.interp(u_dist, dist, path[:,1])
    return np.vstack((x,y)).T

def normalize_path(path: np.ndarray) -> np.ndarray:
    centered = path - np.mean(path, axis=0)
    norm_val = np.linalg.norm(centered)
    return centered / norm_val if norm_val>0 else centered

def _best_circular_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    a, b: (N,2) 로 정규화된 경로
    같은 인덱스끼리 비교하되, 전체 시퀀스를 원형 시프트하며
    평균 거리가 최소가 되는 경우를 찾아 리턴.
    """
    N = len(a)
    best = float('inf')
    for shift in range(N):
        # a 를 shift 한 뒤 b 에 맞춰 평균 L2 거리 계산
        cand = np.roll(a, -shift, axis=0)
        d   = np.linalg.norm(cand - b, axis=1).mean()
        if d < best:
            best = d
    return best

def calculate_similarity_score(
    user_path: np.ndarray,
    gt_path:   np.ndarray,
    num_points: int = 100
) -> tuple[float, float]:
    # 1) 보간
    u = interpolate_path(user_path, num_points)
    g = interpolate_path(gt_path,   num_points)
    # 2) 정규화 (centroid 이동 + scale=1)
    u = normalize_path(u)
    g = normalize_path(g)
    # 3) 최적 원형 시프트 매칭
    avg_dist = _best_circular_distance(u, g)
    # 4) 점수 환산
    score    = max(0, 100 - (avg_dist * 100) ** 2.5)
    return round(score,    2), \
           round(avg_dist, 4), \
            u


import os
import matplotlib.pyplot as plt

def visualize_paths(
    user_path: np.ndarray,
    gt_path:   np.ndarray,
    num_points: int = 100,
    save_dir:   str = "visuals"
) -> tuple[str, str]:
    """
    1) 보간된 원본(interpolated) 경로
    2) 정규화(normalized) 경로
    두 이미지를 save_dir 에 저장하고 파일명을 반환
    """
    # 디렉토리 준비
    os.makedirs(save_dir, exist_ok=True)

    # 1) 보간
    user_interp = interpolate_path(np.array(user_path), num_points)
    gt_interp   = interpolate_path(np.array(gt_path),   num_points)

    # 시각화 1: Interpolated Paths
    fig1, ax1 = plt.subplots()
    ax1.plot(gt_interp[:,0], gt_interp[:,1], label="Ground Truth")
    ax1.plot(user_interp[:,0], user_interp[:,1], label="User Drawing")
    ax1.set_title("Interpolated Paths")
    ax1.legend()
    ax1.axis("equal")
    file1 = os.path.join(save_dir, "paths_interpolated.png")
    fig1.savefig(file1, bbox_inches="tight")
    plt.close(fig1)

    # 2) 정규화
    user_norm = normalize_path(user_interp)
    gt_norm   = normalize_path(gt_interp)

    # 시각화 2: Normalized Paths
    fig2, ax2 = plt.subplots()
    ax2.plot(gt_norm[:,0], gt_norm[:,1], label="Normalized GT")
    ax2.plot(user_norm[:,0], user_norm[:,1], label="Normalized User")
    ax2.set_title("Normalized Paths (centroid=0, scale=1)")
    ax2.legend()
    ax2.axis("equal")
    file2 = os.path.join(save_dir, "paths_normalized.png")
    fig2.savefig(file2, bbox_inches="tight")
    plt.close(fig2)

    return file1, file2
