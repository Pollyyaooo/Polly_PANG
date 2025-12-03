# modules/calibration.py
import time
import adafruit_adxl34x
from adafruit_display_text import label
import terminalio

def zero_offset_calibration(i2c, button, display=None, main_group=None):

    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    
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

    
    def wait_for_button():
        while button.value:  
            time.sleep(0.01)

   
    def perform_zero_offset(samples=20):
        sum_x = sum_y = sum_z = 0
        for _ in range(samples):
            x, y, z = accelerometer.acceleration
            sum_x += x
            sum_y += y
            sum_z += z
            time.sleep(0.05)
        baseline_x = sum_x / samples
        baseline_y = sum_y / samples
        baseline_z = sum_z / samples
        return baseline_x, baseline_y, baseline_z

    
    display_text("Ready to calibrate?\nPress button to start")
    wait_for_button()

    
    display_text("Calibrating...")

   
    baseline_x, baseline_y, baseline_z = perform_zero_offset()

    
    display_text("Calibration complete!")
    time.sleep(2)

    return baseline_x, baseline_y, baseline_z
