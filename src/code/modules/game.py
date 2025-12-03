# game.py
import time
import random
from adafruit_display_text import label
import terminalio
from modules.buzzer_start import buzzer_start
from modules.buzzer_over import buzzer_over
from modules.buzzer_win import buzzer_win
from modules.highscore import load_scores, save_scores, check_new_highscore, insert_new_score, show_highscores
from modules.initials_input import enter_initials
from modules import led_game_over
from modules import led_game_win

# ========== action name ==========
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ACTION_DISPLAY = {"UP": "UP", "DOWN": "DOWN", "LEFT": "LEFT", "RIGHT": "RIGHT"}

# ========== choose difficulty ==========
DIFFICULTY_MULTIPLIER = {"Easy": 1, "Normal": 2, "Hard": 3}
DIFFICULTY_REACTION_TIME = {"Easy": 5.0, "Normal": 3, "Hard": 1.5}

# ========== counter ==========
ACTION_COUNTER = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}

# ========== filter ==========
def low_pass_filter(prev, curr, alpha=0.5):
    return alpha * curr + (1 - alpha) * prev

# ======= motion detect =======

MOTION_IDLE = 0       # 静止阶段
MOTION_ACTION = 1     # 动作峰值阶段
MOTION_RESET = 2      # 回正阶段（忽略所有动作）

motion_state = MOTION_IDLE
last_action = None


def detect_action(accel, baseline,
                  th_y=1.0, th_z=1.0,
                  reset_th=0.4):
   
    global motion_state, last_action

    x, y, z = accel
    bx, by, bz = baseline
    dy = y - by
    dz = z - bz

    # ====== Still ======
    if motion_state == MOTION_IDLE:
        # right
        if dy < -th_y:
            motion_state = MOTION_ACTION
            last_action = "RIGHT"
        # left
        elif dy > th_y:
            motion_state = MOTION_ACTION
            last_action = "LEFT"
        # up
        elif dz > th_z:
            motion_state = MOTION_ACTION
            last_action = "UP"
        # down
        elif dz < -th_z:
            motion_state = MOTION_ACTION
            last_action = "DOWN"
        else:
            return None
        return None  # just start

    # ====== motion biggest =====
    elif motion_state == MOTION_ACTION:
        # leave and back
        if abs(dy) < reset_th and abs(dz) < reset_th:
            motion_state = MOTION_RESET
        return None

    # ====== motion back ======
    elif motion_state == MOTION_RESET:
        # ddefault position
        if abs(dy) < reset_th and abs(dz) < reset_th:
            action = last_action
            motion_state = MOTION_IDLE
            last_action = None
            return action

        return None

# ========== show text ==========
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

# ========== main loop ==========
def play_game(display, main_group, accelerometer, baseline, button, encoder, pixels):
    
    while True:
        # ==================== ddifficulty ====================
        options = ["Easy", "Normal", "Hard"]
        index = 0
        last_position = encoder.position

        def display_difficulty(text):
            while len(main_group) > 0:
                main_group.pop()
            txt_label = label.Label(
                terminalio.FONT,
                text=text,
                color=0xFFFFFF,
                x=0,
                y=display.height // 2 - 4
            )
            main_group.append(txt_label)
            display.refresh()

        display_difficulty(f"Select difficulty:\n{options[index]}")

        while True:
            position = encoder.position
            if position != last_position:
                if position > last_position:
                    index = (index + 1) % len(options)
                else:
                    index = (index - 1) % len(options)
                display_difficulty(f"Select difficulty:\n{options[index]}")
                last_position = position
                time.sleep(0.05)

            if not button.value:
                time.sleep(0.2)
                if not button.value:
                    difficulty_level = options[index]
                    break

        multiplier = DIFFICULTY_MULTIPLIER[difficulty_level]
        reaction_time = DIFFICULTY_REACTION_TIME[difficulty_level]

        # ==================== game start ====================
        score = 0
        show_text(display, main_group, "Game Start")
        buzzer_start()
        time.sleep(1)

        prev_x, prev_y, prev_z = baseline
        game_cleared = True

        for level in range(1, 11):
            actions_count = level * 2 + 2
            level_score = level * 10 * multiplier
            per_action_score = level_score // actions_count

            sequence = [random.choice(ACTIONS) for _ in range(actions_count)]
            show_text(display, main_group, f"LEVEL {level}\nScore {score}")
            time.sleep(0.8)

            for expected in sequence:
                show_text(display, main_group, f"LEVEL {level}\n{ACTION_DISPLAY[expected]}")
                start_t = time.monotonic()
                detected = None

                while time.monotonic() - start_t < reaction_time:
                    x, y, z = accelerometer.acceleration
                    prev_x = low_pass_filter(prev_x, x)
                    prev_y = low_pass_filter(prev_y, y)
                    prev_z = low_pass_filter(prev_z, z)

                    detected = detect_action((prev_x, prev_y, prev_z), baseline)

                    # ==== wrong ====
                    if detected is not None and detected != expected:
                        show_text(display, main_group, "WRONG!")
                        time.sleep(0.6)
                        detected = None
                        break

                    # ==== correct ====
                    if detected == expected:
                        score += per_action_score
                        time.sleep(0.25)  # 冷却，避免回手误判
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

        # ==================== win ====================
        if game_cleared:
            show_text(display, main_group, "YOU WIN!")
            buzzer_win()
            led_game_win.show(pixels)
            time.sleep(2)

        # ==================== final score ====================
        show_text(display, main_group, f"Final Score:{score}")
        time.sleep(1.5)
        
        # ==================== high score ====================
        # compare
        scores = load_scores()
        is_high, index = check_new_highscore(scores, score)

        if is_high:
            
            while len(main_group) > 0:
                main_group.pop()
            show_text(display, main_group, "NEW HIGH SCORE!")
            time.sleep(1)
        
            
            while len(main_group) > 0:
                main_group.pop()
            display.refresh()
        
            
            name = enter_initials(display, main_group, encoder, button)

            
            scores = insert_new_score(scores, index, name, score)
            save_scores(scores)

        
        # ==================== show board ====================
        show_highscores(display, main_group, scores)
        time.sleep(1.5)


        show_text(display, main_group, "Press to restart")
        while button.value:
            time.sleep(0.05)
        while not button.value:
            time.sleep(0.05)
