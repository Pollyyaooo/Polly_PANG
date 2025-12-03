# animations/ball_bounce.py
import displayio
from adafruit_display_text import label
import terminalio
import math
import time

def ball_bounce(display, main_group, paddle_center_x=64, paddle_center_y=42, duration=2.5):
    
    start_time = time.monotonic()

    # color
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF

    screen_width = display.width
    screen_height = display.height

    # circle
    paddle_bitmap = displayio.Bitmap(screen_width, screen_height, 2)
    paddle_grid = displayio.TileGrid(paddle_bitmap, pixel_shader=palette)
    main_group.append(paddle_grid)

    radius_x = 40
    radius_y = 10

    # circle face
    for t in range(0, 360, 1):
        rad = math.radians(t)
        ex = int(paddle_center_x + radius_x * math.cos(rad))
        ey = int(paddle_center_y + radius_y * math.sin(rad))
        if 0 <= ex < screen_width and 0 <= ey < screen_height:
            paddle_bitmap[ex, ey] = 1

    # ball
    circle_layer_size = 16
    circle_bitmap = displayio.Bitmap(circle_layer_size, circle_layer_size, 2)
    circle_grid = displayio.TileGrid(circle_bitmap, pixel_shader=palette,
                                     x=paddle_center_x - circle_layer_size//2,
                                     y=0)
    main_group.append(circle_grid)

    circle_radius = 8
    circle_y = 0
    circle_vy = 0
    gravity = 2
    bounce_factor = -0.7
    pang_displayed = False

    def draw_circle():
        
        for i in range(circle_layer_size):
            for j in range(circle_layer_size):
                circle_bitmap[i, j] = 0
        cx = circle_layer_size // 2
        cy = circle_layer_size // 2
        for dx in range(-circle_radius, circle_radius + 1):
            for dy in range(-circle_radius, circle_radius + 1):
                d2 = dx*dx + dy*dy
                if (circle_radius-1)**2 <= d2 <= circle_radius**2:
                    px = cx + dx
                    py = cy + dy
                    if 0 <= px < circle_layer_size and 0 <= py < circle_layer_size:
                        circle_bitmap[px, py] = 1

    # loop
    while time.monotonic() - start_time < duration:
        # with breathing light
        yield

        circle_vy += gravity
        circle_y += circle_vy

        bottom_limit = paddle_center_y - 5
        if circle_y >= bottom_limit:
            circle_y = bottom_limit
            circle_vy *= bounce_factor

            if not pang_displayed:
                pang_label = label.Label(
                    terminalio.FONT,
                    text="PANG!",
                    color=0xFFFFFF,
                    x=paddle_center_x - 24,
                    y=paddle_center_y - radius_y - 10
                )
                main_group.append(pang_label)
                pang_displayed = True

        circle_grid.y = int(circle_y - circle_layer_size//2)
        draw_circle()
        display.refresh(minimum_frames_per_second=0)
        time.sleep(0.03)

    # stop
    while len(main_group) > 0:
        main_group.pop()

    black_bitmap = displayio.Bitmap(display.width, display.height, 1)
    black_palette = displayio.Palette(1)
    black_palette[0] = 0x000000
    black_grid = displayio.TileGrid(black_bitmap, pixel_shader=black_palette)
    main_group.append(black_grid)
    display.refresh()
