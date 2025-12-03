import time
import board
import busio
import displayio
import i2cdisplaybus
import digitalio
import rotaryio
import neopixel
import adafruit_adxl34x
import adafruit_displayio_ssd1306


from modules import ball_bounce, buzzer_open, led_game_open, calibration, game

# ========== NeoPixel ==========
NUM_PIXELS = 22
pixels = neopixel.NeoPixel(board.D7, NUM_PIXELS, auto_write=False)

# ========== OLED ==========
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
main_group = displayio.Group()
display.root_group = main_group

start_time = time.monotonic()

# ========== button ==========
button = digitalio.DigitalInOut(board.D8)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# ========== Rotary Encoder ==========
encoder = rotaryio.IncrementalEncoder(board.D3, board.D2)  # clk=D3, dt=D2

# ========== accelerometer ==========
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# ========== open ==========
tones = [(440, 0.12), (660, 0.12), (880, 0.12)]
for freq, dur in tones:
    buzzer_open.play_tone(freq, dur, pin=board.D1)
    end_t = time.monotonic() + dur
    while time.monotonic() < end_t:
        led_game_open.breathing_step(pixels, start_time)
        time.sleep(0.005)
    time.sleep(0.03)

animation = ball_bounce.ball_bounce(display, main_group)
for _ in animation:
    led_game_open.breathing_step(pixels, start_time)
    time.sleep(0.005)
led_game_open.turn_off(pixels)

# ========== baseline ==========
baseline_x, baseline_y, baseline_z = calibration.zero_offset_calibration(
    i2c=i2c,
    button=button,
    display=display,
    main_group=main_group
)
print("Baseline:", baseline_x, baseline_y, baseline_z)

# ========== loop ==========
game.play_game(
    display=display,
    main_group=main_group,
    accelerometer=accelerometer,
    baseline=(baseline_x, baseline_y, baseline_z),
    button=button,
    encoder=encoder,
    pixels=pixels
)
