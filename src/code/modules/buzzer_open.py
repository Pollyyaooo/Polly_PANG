import board
import pwmio
import time


VOLUME = 1000   

def play_tone(freq, duration, pin=board.D1):

    buzzer = pwmio.PWMOut(pin, frequency=freq, duty_cycle=VOLUME)
    time.sleep(duration)
    buzzer.deinit()


def boot_beep(pin=board.D1):
    tones = [
        (440, 0.12),
        (660, 0.12),
        (880, 0.12),
    ]

    for freq, dur in tones:
        play_tone(freq, dur, pin)
        time.sleep(0.03)

