# modules/difficulty.py
import time
from adafruit_display_text import label
import terminalio

def choose_difficulty(encoder, button, display=None, main_group=None):

    last_position = encoder.position
    options = ["Easy", "Normal", "Hard"]
    index = 0

    
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

    
    display_text(f"Select difficulty:\n{options[index]}")

    while True:
        
        position = encoder.position
        if position != last_position:
            if position > last_position:
                index = (index + 1) % len(options)
            else:
                index = (index - 1) % len(options)
            display_text(f"Select difficulty:\n{options[index]}")
            last_position = position
            time.sleep(0.05)

        
        if not button.value:  
            time.sleep(0.2)  
            if not button.value:
                return options[index]
