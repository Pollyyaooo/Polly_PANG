# modules/initials_input.py

import time
import terminalio
import rotaryio
from adafruit_display_text import label

def enter_initials(display, main_group, encoder, button):
    
    initials = ["A", "A", "A"]
    position = 0  

    
    letters = [chr(i) for i in range(ord("A"), ord("Z")+1)]
    letter_index = 0

    
    txt_label = label.Label(
        terminalio.FONT,
        text="".join(initials),
        color=0xFFFFFF,
        x=(display.width // 2) - 12,  
        y=(display.height // 2) - 4
    )
    main_group.append(txt_label)
    display.refresh()

    last_encoder_pos = encoder.position

    while position < 3:
        
        delta = encoder.position - last_encoder_pos
        if delta != 0:
            letter_index = (letter_index + delta) % len(letters)
            initials[position] = letters[letter_index]
            txt_label.text = "".join(initials)
            display.refresh()
            last_encoder_pos = encoder.position

        
        if not button.value:  
            time.sleep(0.2) 
            if not button.value:
                position += 1
                letter_index = 0
                encoder.position = 0  
                last_encoder_pos = 0
                time.sleep(0.2)  

        time.sleep(0.02)

    return "".join(initials)
