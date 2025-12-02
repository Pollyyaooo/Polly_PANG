import board
import busio
import displayio
import i2cdisplaybus
import adafruit_displayio_ssd1306
import time
import digitalio
import rotaryio
import neopixel

# 子模块
from modules import ball_bounce, buzzer_open, breathing_light
from modules import calibration, difficulty, game
import adafruit_adxl34x

NUM_PIXELS = 27
pixels = neopixel.NeoPixel(board.D7, NUM_PIXELS, auto_write=False)

# 把 pixels 传给其它模块
from modules import breathing_light
from modules import game
    
# ===== 初始化 OLED =====
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
main_group = displayio.Group()
display.root_group = main_group

start = time.monotonic()

# ===== 初始化按钮 =====
button = digitalio.DigitalInOut(board.D8)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# ===== 初始化加速度计 =====
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# ===== 初始化旋转编码器 =====
encoder = rotaryio.IncrementalEncoder(board.D3, board.D2)  # clk=D3, dt=D2


# ===== 蜂鸣阶段 =====
tones = [(440, 0.12), (660, 0.12), (880, 0.12)]
for freq, dur in tones:
    buzzer_open.play_tone(freq, dur, pin=board.D1)
    end_t = time.monotonic() + dur
    while time.monotonic() < end_t:
        breathing_light.breathing_step(pixels, start)
        time.sleep(0.005)
    time.sleep(0.03)

# ===== 动画阶段（呼吸灯继续） =====
animation = ball_bounce.ball_bounce(display, main_group)
for _ in animation:
    breathing_light.breathing_step(pixels, start)
    time.sleep(0.005)

breathing_light.turn_off(pixels)

# ===== 校准阶段 =====
baseline_x, baseline_y, baseline_z = calibration.zero_offset_calibration(
    i2c=i2c,
    button=button,
    display=display,
    main_group=main_group
)
print("Baseline:", baseline_x, baseline_y, baseline_z)

# ===== 难易阶段 =====
difficulty_level = difficulty.choose_difficulty(
    encoder=encoder,
    button=button,
    display=display,
    main_group=main_group
)

# ===== 游戏流程 =====
final_score = game.play_game(
    display=display,
    main_group=main_group,
    accelerometer=accelerometer,
    baseline=(baseline_x, baseline_y, baseline_z),
    button=button,
    encoder=encoder,
    pixels=pixels,
    difficulty_level=difficulty_level
)

print("Final Score:", final_score)
