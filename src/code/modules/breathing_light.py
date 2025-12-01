import neopixel
import math
import time
import board

num_pixels = 27
pixels = neopixel.NeoPixel(board.D7, num_pixels, auto_write=False)

# 呼吸灯参数
brightness_max = 1.0
brightness_min = 0.05
breath_period = 2.0

def breathing_step(start_time):
    """执行一次呼吸灯更新，用于主程序循环调用"""

    t = time.monotonic() - start_time
    brightness = (math.sin(2 * math.pi * t / breath_period) + 1)/2
    brightness = brightness_min + (brightness_max - brightness_min) * brightness

    for i in range(num_pixels):
        pixels[i] = (int(255 * brightness), int(255 * brightness), int(255 * brightness))
    pixels.show()

def turn_off():
    """关闭灯"""
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()
