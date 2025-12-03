import board
import pwmio
import time

VOLUME = 5000

def play_tone(freq, duration, pin=board.D1):
    buzzer = pwmio.PWMOut(pin, frequency=freq, duty_cycle=VOLUME)
    time.sleep(duration)
    buzzer.deinit()

def buzzer_over(pin=board.D1):
    tones = [
        (330, 0.2),  # E4
        (196, 0.25)  # G3
    ]
    for freq, dur in tones:
        play_tone(freq, dur, pin)
        time.sleep(0.05)

