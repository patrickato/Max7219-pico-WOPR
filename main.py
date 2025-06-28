# ========== FULL INTEGRATED CODE WITH SHOCKWAVE ==========
from machine import Pin, SPI
import max7219
import random
import math
from time import sleep, time

# ========== Configuration ==========
DEBUG = True
REVERSE_PANEL_ORDER = False

DEFCON_DURATIONS = [600, 600, 600, 600, 600]
DEFCON_SETTINGS = [
    (0.75, 300),  # DEFCON 5
    (0.45, 400),  # DEFCON 4
    (0.225, 500), # DEFCON 3
    (0.08, 600),  # DEFCON 2
    (0.025, 700), # DEFCON 1
]

# ========== Setup SPI and Display ==========
spi = SPI(0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 8)
display.brightness(2)

# ========== Messages ==========
greeting_message = " Greetings Professor Falken, You Are A Hard Man to Reach "
flash_messages = ["Shall We", "Play A", "Game?"]
defcon_levels = ["DEFCON 5", "DEFCON 4", "DEFCON 3", "DEFCON 2", "DEFCON 1"]
shutdown_message = "SHUTDOWN"
rebooting_message = " REBOOTING "
system_override_message = "System Override In Progress. Please Wait..."
code_search_init_message = "Code Search Protocol Initializing..."
system_starting_message = "System Starting Please Wait..."
characters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*+=[]{}?")

# ========== Utility Functions ==========
def log(msg):
    if DEBUG:
        print(msg)

def shuffle_list(lst):
    shuffled = lst[:]
    for i in range(len(shuffled) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

def draw_char_at(char, panel_index):
    actual_index = 7 - panel_index if REVERSE_PANEL_ORDER else panel_index
    display.text(char, actual_index * 8, 0, 1)

# ========== Visual Effects ==========
def scroll_text(msg, speed=0.015):
    text_width = len(msg) * 8
    for offset in range(-64, text_width):
        display.fill(0)
        display.text(msg, -offset, 0, 1)
        display.show()
        sleep(speed)

def flash_message(msg, flash_speed=0.5):
    display.fill(0)
    display.show()
    sleep(flash_speed)
    display.text(msg, 0, 0, 1)
    display.show()
    sleep(flash_speed)

def slide_defcon_message(msg, speed=0.015, pause_time=3):
    text_width = len(msg) * 8
    for offset in range(-64, text_width):
        display.fill(0)
        display.text(msg, -offset, 0, 1)
        display.show()
        sleep(speed)
        if offset == (text_width - 64):
            display.text(msg, 0, 0, 1)
            display.show()
            sleep(pause_time)
            break

def update_flickering(flicker_speed, flicker_intensity):
    display.fill(0)
    for _ in range(flicker_intensity):
        x, y = random.randint(0, 63), random.randint(0, 7)
        display.pixel(x, y, random.randint(0, 1))
    display.show()
    sleep(flicker_speed)

# ========== Missile and Shockwave ==========
class Missile:
    def __init__(self, start_x):
        self.x = float(start_x)
        self.y = 7.0
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-1.2, -1.5)
        self.state = 'rising'
        self.explode_ticks = 0
        self.shockwave_radius = 0
        self.impact_x = 0
        self.impact_y = 7

    def update(self):
        gravity = 0.07
        if self.state == 'rising':
            self.x += self.vx
            self.y += self.vy
            self.vy += gravity
            if self.vy >= 0:
                self.state = 'falling'
        elif self.state == 'falling':
            self.x += self.vx
            self.y += self.vy
            self.vy += gravity
            if self.y >= 7:
                self.y = 7
                self.state = 'exploding'
                self.explode_ticks = 0
                self.impact_x = int(self.x)
                self.impact_y = 7
        elif self.state == 'exploding':
            self.explode_ticks += 1
            if self.explode_ticks > 12:
                self.state = 'shockwave'
                self.shockwave_radius = 0
        elif self.state == 'shockwave':
            self.shockwave_radius += 1
            if self.shockwave_radius > 8:
                return False
        return True

    def draw(self):
        if self.state in ['rising', 'falling']:
            x, y = int(self.x), int(self.y)
            if 0 <= x < 64 and 0 <= y < 8:
                display.pixel(x, y, 1)
        elif self.state == 'exploding':
            for _ in range(15):
                dx = random.randint(-2, 2)
                dy = random.randint(-2, 0)
                px = self.impact_x + dx
                py = self.impact_y + dy
                if 0 <= px < 64 and 0 <= py < 8:
                    display.pixel(px, py, random.choice([0,1]))
        elif self.state == 'shockwave':
            r = self.shockwave_radius
            cx, cy = self.impact_x, self.impact_y
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                px = int(cx + r * math.cos(rad))
                py = int(cy + r * math.sin(rad))
                if 0 <= px < 64 and 0 <= py < 8:
                    display.pixel(px, py, 1)

def run_missile_sequence():
    missiles = []
    launch_delay = 0
    max_missiles = 12
    frame_limit = 200
    frame = 0

    while frame < frame_limit:
        display.fill(0)
        if launch_delay <= 0 and len(missiles) < max_missiles:
            start_x = random.randint(8, 56)
            missiles.append(Missile(start_x))
            launch_delay = random.randint(3, 7)
        else:
            launch_delay -= 1

        alive = []
        for m in missiles:
            if m.update():
                m.draw()
                alive.append(m)
        missiles = alive

        display.show()
        sleep(0.05)
        frame += 1

    impact_shockwave()  # NEW FINAL SHOCKWAVE

def impact_shockwave():
    cx = 31
    cy = 3
    for radius in range(1, 6):
        display.fill(0)
        for x in range(64):
            for y in range(8):
                dx = x - cx
                dy = y - cy
                dist = (dx**2 + dy**2)**0.5
                if abs(dist - radius) < 0.75:
                    display.pixel(x, y, 1)
        display.show()
        sleep(0.05)
    for _ in range(3):
        display.fill(1)
        display.show()
        sleep(0.05)
        display.fill(0)
        display.show()
        sleep(0.05)

# ========== Shutdown + Reboot ==========
def shutdown_sequence():
    for _ in range(3):
        display.fill(0)
        for i, char in enumerate(shutdown_message):
            draw_char_at(char, i)
        display.show()
        sleep(0.2)
        for _ in range(8):
            for i in range(len(shutdown_message)):
                for x in range(8):
                    for y in range(8):
                        px = x + i * 8
                        display.pixel(px, y, 1 - display.pixel(px, y))
            display.show()
            sleep(0.2)
    display.fill(0)
    display.show()
    sleep(2)
    scroll_text(rebooting_message, speed=0.03)

# ========== Code Search ==========
def flash_code_sequence(code_sequence):
    for _ in range(25):
        display.fill(0)
        for i, char in enumerate(code_sequence):
            draw_char_at(char, i)
        display.show()
        sleep(0.2)
        for i in range(8):
            for x in range(8):
                for y in range(8):
                    px = x + i * 8
                    display.pixel(px, y, 1 - display.pixel(px, y))
        display.show()
        sleep(0.2)

def display_code_search():
    current_code = [""] * 8
    locked_panels = [False] * 8
    lock_order = shuffle_list(list(range(8)))
    lock_times = [time() + random.uniform(18, 42) for _ in range(8)]
    lock_count = 0
    code_sequence = ''.join(random.choice(characters) for _ in range(8))
    log(f"Generated code: {code_sequence}")

    start_time, last_lock_time = time(), time()
    lock_intervals = [random.uniform(18, 42) for _ in range(8)]

    while time() - start_time < 300:
        current_code = [random.choice(characters) if not locked_panels[i] else current_code[i] for i in range(8)]
        display.fill(0)
        for i, char in enumerate(current_code):
            draw_char_at(char, i)
        display.show()
        sleep(0.015)

        for i in range(8):
            if not locked_panels[i] and time() >= lock_times[i]:
                if time() - last_lock_time >= lock_intervals[i]:
                    lock_index = lock_order[lock_count]
                    current_code[lock_index] = code_sequence[lock_index]
                    locked_panels[lock_index] = True
                    lock_count += 1
                    last_lock_time = time()
                    log(f"Locked box {lock_index+1} with {code_sequence[lock_index]}")

        if lock_count == 8:
            flash_code_sequence(code_sequence)
            run_missile_sequence()
            shutdown_sequence()
            return
        sleep(0.03)

# ========== State Machine ==========
def run_state(state):
    if state == "STARTUP":
        log("STARTUP")
        scroll_text(system_starting_message, speed=0.05)
    elif state == "GREETING":
        log("GREETING")
        scroll_text(greeting_message)
    elif state == "FLASH":
        log("FLASH MESSAGES")
        for msg in flash_messages:
            flash_message(msg)
            sleep(0.25)
    elif state == "DEFCON":
        log("DEFCON PHASE")
        for i, defcon_msg in enumerate(defcon_levels):
            slide_defcon_message(defcon_msg, speed=0.015, pause_time=3)
            flicker_speed, flicker_intensity = DEFCON_SETTINGS[i]
            start = time()
            while time() - start < DEFCON_DURATIONS[i]:
                update_flickering(flicker_speed, flicker_intensity)
    elif state == "OVERRIDE":
        log("OVERRIDE MODE")
        scroll_text(system_override_message, speed=0.015)
        scroll_text(code_search_init_message, speed=0.015)
    elif state == "CODE":
        log("CODE SEARCH MODE")
        display_code_search()

# ========== Main Loop ==========
def main_loop():
    sequence = ["STARTUP", "GREETING", "FLASH", "DEFCON", "OVERRIDE", "CODE"]
    while True:
        for state in sequence:
            run_state(state)

main_loop()
