# breathing_light.py

import time
import math

def breathing_step(pixels, start_time):
    brightness = (math.sin((time.monotonic() - start_time) * 3) + 1) / 2
    brightness = 0.05 + brightness * 0.95

    for i in range(len(pixels)):
        pixels[i] = (int(255 * brightness), int(255 * brightness), int(255 * brightness))
    pixels.show()

def turn_off(pixels):
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 0)
    pixels.show()
