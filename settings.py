"""Numbers and colors shared by the game.

Keeping these in one file means the window size, speed, and colors
are easy to find and change later without hunting through the game loop.
"""

# Size of the game window, in pixels.
WIDTH = 960
HEIGHT = 540

# Frames per second. The game loop tries to run this many times each second.
FPS = 60

# Text shown in the title bar of the window.
TITLE = "Airplane Game"

WHITE = (255, 255, 255)

# The picture is an airplane. This circle is what lands, hits hazards, and reaches the goal.
PLAYER_RADIUS = 22
PLAYER_SPEED = 5
JUMP_STRENGTH = -12
GRAVITY = 0.5

# Nose tilt follows vertical speed. The cap keeps the lean small.
# TILT_EASE is how much of the remaining gap is closed each frame.
TILT_MAX = 14
TILT_EASE = 0.15

# Floating platforms share one thickness. Each one is (x, top, width).
PLATFORM_THICKNESS = 16

# Each level gets 3 lives. Reaching the next level fills them again.
STARTING_LIVES = 3
RAIN_COLOR = (185, 195, 215)

# The home flag stands on the last platform of each level.
GOAL_HEIGHT = 90
GOAL_RED = (196, 36, 42)
POLE = (225, 232, 240)

# clouds and planes are the hazards. Every cloud in these lists costs a life.
# planes are (x, y, min_x, max_x, speed).
# Vertical gaps stay within the jump: about 80 on level 1, 100 on level 2, 115 on level 3.
LEVELS = [
    {
        "name": "Above the Clouds",
        "sky_top": (0, 150, 245),
        "sky_bottom": (90, 205, 255),
        "ink": WHITE,
        "sun_glow": ((255, 226, 120), (860, 100), 70),
        "sun": ((255, 206, 60), (860, 100), 40),
        "fog": None,
        "rain": False,
        "platform": (255, 255, 255),
        "platform_edge": (0, 105, 195),
        "start_x": 120,
        "platforms": [
            (40, 480, 300),
            (420, 400, 260),
            (700, 310, 220),
        ],
        "clouds": [
            (640, 328, 56, 26),
        ],
        "planes": [
            (500, 210, 430, 900, 2),
        ],
    },
    {
        "name": "Sunset Flight",
        "sky_top": (255, 112, 32),
        "sky_bottom": (255, 186, 128),
        "ink": WHITE,
        "sun_glow": ((255, 214, 90), (160, 280), 96),
        "sun": ((255, 196, 40), (160, 280), 54),
        "fog": None,
        "rain": False,
        "platform": (255, 255, 255),
        "platform_edge": (196, 82, 16),
        "start_x": 70,
        "platforms": [
            (20, 500, 150),
            (240, 410, 110),
            (450, 310, 100),
            (220, 210, 100),
            (40, 120, 120),
            (280, 160, 90),
            (400, 90, 160),
            (660, 180, 220),
        ],
        "clouds": [
            (220, 428, 50, 24),
            (400, 428, 48, 22),
            (140, 250, 46, 22),
            (548, 140, 48, 22),
        ],
        "planes": [
            (300, 332, 180, 720, 2),
            (80, 250, 40, 400, -2),
            (360, 228, 250, 860, 2),
        ],
    },
    {
        "name": "The Storm",
        "sky_top": (14, 22, 58),
        "sky_bottom": (62, 40, 96),
        "ink": WHITE,
        "sun_glow": ((150, 160, 185), (88, 210), 36),
        "sun": ((196, 204, 220), (88, 210), 18),
        "fog": (70, 76, 98, 70),
        "rain": True,
        "platform": (255, 255, 255),
        "platform_edge": (90, 130, 175),
        "start_x": 70,
        "platforms": [
            (24, 500, 130),
            (210, 385, 100),
            (400, 270, 90),
            (230, 160, 90),
            (430, 90, 90),
            (640, 160, 90),
            (820, 110, 110),
        ],
        "clouds": [
            (200, 430, 44, 20),
            (320, 308, 44, 20),
            (490, 198, 42, 20),
            (700, 318, 44, 20),
            (450, 120, 42, 20),
        ],
        "planes": [
            (180, 308, 140, 700, 3),
            (200, 428, 120, 780, 2),
            (240, 16, 140, 380, -2),
        ],
    },
]
