import board
import pwmio
import time

VOLUME = 5000

def play_tone(freq, duration, pin=board.D1):
    buzzer = pwmio.PWMOut(pin, frequency=freq, duty_cycle=VOLUME)
    time.sleep(duration)
    buzzer.deinit()

def buzzer_win(pin=board.D1):
    tones = [
        (659, 0.15),  # E5
        (784, 0.15),  # G5
        (988, 0.18)   # B5
    ]
    for freq, dur in tones:
        play_tone(freq, dur, pin)
        time.sleep(0.04)
