import time

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    pos -= 170
    return (0, pos * 3, 255 - pos * 3)

def show(pixels):
    n = len(pixels)
    for j in range(256):
        for i in range(n):
            idx = (i * 256 // n) + j
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(0.02)
