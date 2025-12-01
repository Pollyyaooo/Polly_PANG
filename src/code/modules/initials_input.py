# modules/initials_input.py

import time
import terminalio
import rotaryio
from adafruit_display_text import label

def enter_initials(display, main_group, encoder, button):
    """
    输入玩家 initials，用于 High Score
    display / main_group：OLED 显示
    encoder：rotaryio.IncrementalEncoder 对象
    button：DigitalInOut 按钮对象
    返回：3 个字母的字符串
    """
    initials = ["A", "A", "A"]
    position = 0  # 当前编辑字母位置

    # 字母表
    letters = [chr(i) for i in range(ord("A"), ord("Z")+1)]
    letter_index = 0

    # ===== 初始化 Label 并加入 main_group =====
    txt_label = label.Label(
        terminalio.FONT,
        text="".join(initials),
        color=0xFFFFFF,
        x=(display.width // 2) - 12,  # 居中
        y=(display.height // 2) - 4
    )
    main_group.append(txt_label)
    display.refresh()

    last_encoder_pos = encoder.position

    while position < 3:
        # ===== 检测旋钮变化 =====
        delta = encoder.position - last_encoder_pos
        if delta != 0:
            letter_index = (letter_index + delta) % len(letters)
            initials[position] = letters[letter_index]
            txt_label.text = "".join(initials)
            display.refresh()
            last_encoder_pos = encoder.position

        # ===== 按钮确认当前字母 =====
        if not button.value:  # 按下为 False
            time.sleep(0.2)  # 消抖
            if not button.value:
                position += 1
                letter_index = 0
                encoder.position = 0  # 重置旋钮
                last_encoder_pos = 0
                time.sleep(0.2)  # 防止误触

        time.sleep(0.02)

    return "".join(initials)
