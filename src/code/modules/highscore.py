# modules/highscore.py
import microcontroller
import json

NVM_SIZE = 128  # enough
EMPTY_DATA = {
    "scores": [
        {"score": 0, "name": "---"},
        {"score": 0, "name": "---"},
        {"score": 0, "name": "---"}
    ]
}

def load_scores():
    raw = bytes(microcontroller.nvm[:NVM_SIZE]).decode().strip("\x00").strip()
    if not raw:
        return EMPTY_DATA["scores"]
    try:
        data = json.loads(raw)
        return data["scores"]
    except:
        return EMPTY_DATA["scores"]


def save_scores(scores):
    data_str = json.dumps({"scores": scores})
    data_bytes = data_str.encode()

    if len(data_bytes) > NVM_SIZE:
        raise ValueError("High score data too large")

    # 写入
    microcontroller.nvm[:NVM_SIZE] = b"\x00" * NVM_SIZE
    microcontroller.nvm[:len(data_bytes)] = data_bytes


def check_new_highscore(scores, new_score):
    """
    return (True, index) if new highscore
    return (False, None) otherwise
    """
    for i, entry in enumerate(scores):
        if new_score > entry["score"]:
            return True, i
    return False, None


def insert_new_score(scores, index, name, score):
    scores.insert(index, {"name": name, "score": score})
    return scores[:3]  # keep only top 3
