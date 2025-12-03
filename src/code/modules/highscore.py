# modules/highscore.py
import microcontroller
import json
import time
from adafruit_display_text import label
import terminalio

  
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


def show_highscores(display, main_group, scores):

    while len(main_group) > 0:
        main_group.pop()

    title_label = label.Label(
        terminalio.FONT,
        text="HIGH SCORES",
        color=0xFFFFFF,
        x=0,
        y=10  
    )
    main_group.append(title_label)


    top_margin = 20  
    line_height = 10  
    for i, entry in enumerate(scores):
        txt = label.Label(
            terminalio.FONT,
            text=f"{i+1}. {entry['name']}  {entry['score']}",
            color=0xFFFFFF,
            x=0,
            y=top_margin + i * line_height
        )
        main_group.append(txt)

    display.refresh()
    time.sleep(3)  
