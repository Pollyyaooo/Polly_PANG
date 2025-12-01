import board
import pwmio
import time

VOLUME = 1000  # 主音量，可调 0~65535

def play_tone(freq, duration, pin=board.D1):
    buzzer = pwmio.PWMOut(pin, frequency=freq, duty_cycle=VOLUME)
    time.sleep(duration)
    buzzer.deinit()

def buzzer_start(pin=board.D1):
    tones = [
        (523, 0.12),  # C5
        (659, 0.12),  # E5
        (784, 0.12),  # G5
    ]

    for freq, dur in tones:
        play_tone(freq, dur, pin)
        time.sleep(0.03)
