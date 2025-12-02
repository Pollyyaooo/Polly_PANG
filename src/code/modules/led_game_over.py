import time

def show(pixels):
    for _ in range(2):
        # yellow flash
        for i in range(len(pixels)):
            pixels[i] = (255, 255, 0)
        pixels.show()
        time.sleep(0.15)

        # dark
        for i in range(len(pixels)):
            pixels[i] = (0, 0, 0)
        pixels.show()
        time.sleep(0.1)
