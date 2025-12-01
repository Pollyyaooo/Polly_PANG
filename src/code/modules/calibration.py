# modules/calibration.py
import time
import adafruit_adxl34x
from adafruit_display_text import label
import terminalio

def zero_offset_calibration(i2c, button, display=None, main_group=None):
    """
    完整零点偏移校准
    返回: baseline_x, baseline_y, baseline_z
    """
    # 初始化加速度计
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    # 辅助函数：显示文字
    def display_text(text):
        if display is None or main_group is None:
            print(text)
            return
        # 清屏
        while len(main_group) > 0:
            main_group.pop()
        text_label = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF,
            x=0,
            y=display.height // 2 - 4
        )
        main_group.append(text_label)
        display.refresh()

    # 等待按钮按下
    def wait_for_button():
        while button.value:  # 按钮未按下为 True
            time.sleep(0.01)

    # 采样计算 baseline
    def perform_zero_offset(samples=20):
        sum_x = sum_y = sum_z = 0
        for _ in range(samples):
            x, y, z = accelerometer.acceleration
            sum_x += x
            sum_y += y
            sum_z += z
            time.sleep(0.05)
        baseline_x = sum_x / samples
        baseline_y = sum_y / samples
        baseline_z = sum_z / samples
        return baseline_x, baseline_y, baseline_z

    # 1️⃣ 提示准备校准
    display_text("Ready to calibrate?\nPress button to start")
    wait_for_button()

    # 2️⃣ 显示校准中
    display_text("Calibrating...")

    # 3️⃣ 进行零点偏移校准
    baseline_x, baseline_y, baseline_z = perform_zero_offset()

    # 4️⃣ 校准完成提示
    display_text("Calibration complete!")
    time.sleep(2)

    return baseline_x, baseline_y, baseline_z
