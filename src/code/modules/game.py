import time
import random
from adafruit_display_text import label
import terminalio
from modules.buzzer_start import buzzer_start
from modules.buzzer_over import buzzer_over
from modules.buzzer_win import buzzer_win
from modules.highscore import load_scores, save_scores, check_new_highscore, insert_new_score
from modules.initials_input import enter_initials
from modules import led_game_over
from modules import led_game_win


ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


ACTION_DISPLAY = {
    "UP": "UP",
    "DOWN": "DOWN",
    "LEFT": "LEFT",
    "RIGHT": "RIGHT"
}

# ========= 难度设定 =========
DIFFICULTY_MULTIPLIER = {
    "Easy": 1,
    "Normal": 2,
    "Hard": 3
}

DIFFICULTY_REACTION_TIME = {
    "Easy": 5.0,
    "Normal": 3.0,
    "Hard": 1.0
}

# ========= 动作计数器 =========
ACTION_COUNTER = {
    "UP": 0,
    "DOWN": 0,
    "LEFT": 0,
    "RIGHT": 0
}

# ========= 低通滤波 =========
def low_pass_filter(prev, curr, alpha=0.5):
    return alpha * curr + (1 - alpha) * prev


# ========= 动作检测 =========
def detect_action(accel, baseline,
                  threshold_y=0.5, threshold_z=0.5,
                  hold_frames=1):

    x, y, z = accel
    bx, by, bz = baseline

    dy = y - by
    dz = z - bz

    
    for k in ACTION_COUNTER:
        ACTION_COUNTER[k] = max(0, ACTION_COUNTER[k] - 1)

    
    if dy > threshold_y:
        ACTION_COUNTER["LEFT"] += 1
    elif dy < -threshold_y:
        ACTION_COUNTER["RIGHT"] += 1

   
    if dz > threshold_z:
        ACTION_COUNTER["UP"] += 1
    elif dz < -threshold_z:
        ACTION_COUNTER["DOWN"] += 1

   
    for action, count in ACTION_COUNTER.items():
        if count >= hold_frames:
            for k in ACTION_COUNTER:
                ACTION_COUNTER[k] = 0
            return action

    return None



def show_text(display, main_group, text, y_offset=0):
    while len(main_group) > 0:
        main_group.pop()

    txt = label.Label(
        terminalio.FONT,
        text=text,
        color=0xFFFFFF,
        x=0,
        y=(display.height // 2 - 4) + y_offset
    )

    main_group.append(txt)
    display.refresh()



def play_game(display, main_group, accelerometer, baseline, button, encoder, pixels, difficulty_level="Easy"):

    multiplier = DIFFICULTY_MULTIPLIER[difficulty_level]
    reaction_time = DIFFICULTY_REACTION_TIME[difficulty_level]

    while True:
        score = 0
        show_text(display, main_group, "Game Start")
        buzzer_start()
        time.sleep(1)

        prev_x, prev_y, prev_z = baseline
        game_cleared = True  # 默认通关

        
        for level in range(1, 11):
            actions_count = level * 2 + 2
            level_score = level * 10 * multiplier
            per_action_score = level_score // actions_count

            sequence = [random.choice(ACTIONS) for _ in range(actions_count)]

            show_text(display, main_group, f"LEVEL {level}\nScore {score}")
            time.sleep(0.8)

            # ===== 每一步动作 =====
            for expected in sequence:

                
                show_text(
                    display,
                    main_group,
                    f"LEVEL {level}\n{ACTION_DISPLAY[expected]}"
                )

                start_t = time.monotonic()
                detected = None


                while time.monotonic() - start_t < reaction_time:

                    x, y, z = accelerometer.acceleration

                    prev_x = low_pass_filter(prev_x, x)
                    prev_y = low_pass_filter(prev_y, y)
                    prev_z = low_pass_filter(prev_z, z)

                    detected = detect_action(
                        (prev_x, prev_y, prev_z),
                        baseline,
                        threshold_y=0.2,
                        threshold_z=0.2,
                        hold_frames=1
                    )

                    if detected == expected:
                        score += per_action_score
                        time.sleep(0.2)
                        break

                    time.sleep(0.02)

                if detected != expected:
                    show_text(display, main_group, "GAME OVER")
                    buzzer_over()
                    led_game_over.show(pixels)
                    time.sleep(1.5)
                    game_cleared = False
                    break

            else:
                show_text(display, main_group, f"Level {level} OK!\nScore:{score}")
                time.sleep(1.0)
                continue

            break

        
        if game_cleared:
            show_text(display, main_group, "YOU WIN!")
            buzzer_win()
            led_game_win.show(pixels)
            time.sleep(2)

        # ======= 检查是否为新高分 =======
        scores = load_scores()
        is_high, index = check_new_highscore(scores, score)

        if is_high:
            
            show_text(display, main_group, "NEW HIGH SCORE!")
            time.sleep(1)

            
            while len(main_group) > 0:
                main_group.pop()

           
            name = enter_initials(display, main_group, encoder, button)

            
            scores = insert_new_score(scores, index, name, score)
            save_scores(scores)

        
        
        show_text(display, main_group, f"Final Score:{score}")
        time.sleep(1.5)

        
        scores = load_scores()
        board_text = "HIGH SCORES:\n"
        for entry in scores:
            board_text += f"{entry['name']}  {entry['score']}\n"

        show_text(display, main_group, board_text)
        time.sleep(3)

        
        show_text(display, main_group, f"Final Score:{score}")
        time.sleep(1.5)

        show_text(display, main_group, "Press to restart")

        while button.value:
            time.sleep(0.05)
        while not button.value:
            time.sleep(0.05)
