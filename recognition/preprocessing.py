import numpy as np

def normalize_landmarks(landmark_list):
    if not landmark_list:
        return []
    if isinstance(landmark_list[0], (int, float)):
        coords = np.array(landmark_list, dtype=np.float32).reshape(-1, 3)
    else:
        coords = np.array([[lm[1], lm[2], lm[3]] for lm in landmark_list], dtype=np.float32)
    base = coords[0]
    coords = coords - base
    max_val = np.max(np.abs(coords))
    if max_val > 0:
        coords = coords / max_val
    return coords.flatten().tolist()
