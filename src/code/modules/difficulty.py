# modules/difficulty.py
import time
from adafruit_display_text import label
import terminalio

def choose_difficulty(encoder, button, display=None, main_group=None):
    """
    使用旋钮选择难易度：
    - encoder：已经初始化好的 rotaryio.IncrementalEncoder 对象
    - button：DigitalInOut对象，用作确认按钮（D8）
    - display / main_group：显示文字（可选）
    返回：选中的难易度字符串
    """
    last_position = encoder.position
    options = ["Easy", "Normal", "Hard"]
    index = 0

    # 显示文字辅助函数
    def display_text(text):
        if display is None or main_group is None:
            print(text)
            return
        while len(main_group) > 0:
            main_group.pop()
        text_label = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF,
            x=0,
            y=display.height // 2 - 4
        )
        main_group.append(text_label)
        display.refresh()

    # 初始显示
    display_text(f"Select difficulty:\n{options[index]}")

    while True:
        # 旋钮变化检测
        position = encoder.position
        if position != last_position:
            if position > last_position:
                index = (index + 1) % len(options)
            else:
                index = (index - 1) % len(options)
            display_text(f"Select difficulty:\n{options[index]}")
            last_position = position
            time.sleep(0.05)

        # 按钮确认
        if not button.value:  # 按下为 False
            time.sleep(0.2)  # 去抖动
            if not button.value:
                return options[index]
