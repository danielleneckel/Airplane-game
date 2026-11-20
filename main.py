"""Airplane game.

Run this file on your computer:

    python3 main.py

Pygbag also uses this file as the entry point for a later browser build.
The same Python code runs in both places.
"""

import asyncio
import random

import pygame

from player import Player
from settings import (
    FPS,
    GOAL_HEIGHT,
    GOAL_RED,
    HEIGHT,
    LEVELS,
    PLATFORM_THICKNESS,
    PLAYER_RADIUS,
    POLE,
    RAIN_COLOR,
    STARTING_LIVES,
    TITLE,
    WHITE,
    WIDTH,
)


class OtherPlane:
    """A small pastel airplane that flies back and forth."""

    WIDTH = 56
    HEIGHT = 22

    def __init__(self, x, y, min_x, max_x, speed):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self):
        self.x += self.speed
        if self.x < self.min_x or self.x + self.WIDTH > self.max_x:
            self.speed = -self.speed
            self.x += self.speed

    def draw(self, screen):
        facing = 1 if self.speed >= 0 else -1
        cx = self.x + self.WIDTH // 2
        cy = self.y + self.HEIGHT // 2

        def at(dx, dy):
            return (cx + facing * dx, cy + dy)

        # Bright blue so these planes read clearly on every sky.
        color = (40, 175, 255)
        outline = (0, 120, 230)
        wing = [at(-4, 2), at(10, 2), at(6, 9), at(-8, 8)]
        tail = [at(-16, -3), at(-10, -12), at(-4, -3)]
        body = [at(-20, -4), at(8, -5), at(22, 0), at(8, 5), at(-20, 4)]
        pygame.draw.polygon(screen, color, wing)
        pygame.draw.polygon(screen, outline, wing, 2)
        pygame.draw.polygon(screen, color, tail)
        pygame.draw.polygon(screen, outline, tail, 2)
        pygame.draw.polygon(screen, color, body)
        pygame.draw.polygon(screen, outline, body, 2)
        pygame.draw.circle(screen, (255, 214, 70), at(14, 0), 3)


def make_platforms(layout):
    """Build platform rectangles from one level's list of (x, top, width)."""
    platforms = []
    for x, top, width in layout:
        platforms.append(pygame.Rect(x, top, width, PLATFORM_THICKNESS))
    return platforms


def make_clouds(layout):
    return [pygame.Rect(cloud) for cloud in layout]


def make_fog(color):
    """A see-through sheet. None means this level has no fog."""
    if not color:
        return None
    fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fog.fill(color)
    return fog


def build_level(index):
    """Turn one entry in LEVELS into the rectangles the game loop uses."""
    level = LEVELS[index]
    start = (level["start_x"], level["platforms"][0][1] - PLAYER_RADIUS)
    planes = [OtherPlane(*plane) for plane in level["planes"]]
    return {
        "level": level,
        "platforms": make_platforms(level["platforms"]),
        "clouds": make_clouds(level["clouds"]),
        "planes": planes,
        "fog": make_fog(level["fog"]),
        "start": start,
    }


def make_rain():
    drops = []
    for _ in range(40):
        drops.append(
            [random.randrange(WIDTH), random.randrange(HEIGHT), random.randint(7, 12)]
        )
    return drops


def player_box(player):
    """The rectangle around the airplane's collision circle."""
    return pygame.Rect(
        player.x - PLAYER_RADIUS,
        player.y - PLAYER_RADIUS,
        PLAYER_RADIUS * 2,
        PLAYER_RADIUS * 2,
    )


def goal_rect(home_platform):
    """The flag area above the goal platform.

    The rectangle continues a little below the platform top, so landing
    under the flag counts. A rectangle that only touches an edge does not.
    """
    return pygame.Rect(
        home_platform.right - 70,
        home_platform.top - GOAL_HEIGHT,
        56,
        GOAL_HEIGHT + 24,
    )


def draw_background(screen, level):
    """Paint a vertical sky gradient, then the sun if this level has one."""
    top = level["sky_top"]
    bottom = level["sky_bottom"]
    for band in range(0, HEIGHT, 3):
        blend = band / HEIGHT
        color = tuple(int(top[channel] + (bottom[channel] - top[channel]) * blend) for channel in range(3))
        pygame.draw.rect(screen, color, (0, band, WIDTH, 3))
    if level["sun_glow"]:
        glow_color, glow_center, glow_radius = level["sun_glow"]
        pygame.draw.circle(screen, glow_color, glow_center, glow_radius)
    if level["sun"]:
        sun_color, sun_center, sun_radius = level["sun"]
        pygame.draw.circle(screen, sun_color, sun_center, sun_radius)


def draw_rain(screen, drops):
    for x, y, _speed in drops:
        pygame.draw.line(screen, RAIN_COLOR, (x, y), (x - 2, y + 10), 1)


def update_rain(drops):
    for drop in drops:
        drop[1] += drop[2]
        if drop[1] > HEIGHT:
            drop[0] = random.randrange(WIDTH)
            drop[1] = -10


def draw_platforms(screen, platforms, level):
    for platform in platforms:
        pygame.draw.rect(screen, level["platform"], platform)
        pygame.draw.rect(screen, level["platform_edge"], platform, 2)


def draw_cloud(screen, cloud):
    """Draw one white hazard cloud with a bright outline so it stays visible."""
    shadow = (20, 55, 110)
    fill = (255, 255, 255)
    outline = (0, 100, 185)
    center_y = cloud.centery
    radius = cloud.height // 2
    points = (
        (cloud.left + radius, center_y),
        (cloud.centerx, center_y - 4),
        (cloud.right - radius, center_y),
    )
    for point in points:
        pygame.draw.circle(screen, shadow, (point[0] + 2, point[1] + 3), radius)
    for point in points:
        pygame.draw.circle(screen, fill, point, radius)
        pygame.draw.circle(screen, outline, point, radius, 2)


def draw_goal(screen, font, home_platform):
    """Draw a flagpole and a red flag labeled HOME.

    The font is a smaller Arial so the word sits fully inside the flag.
    """
    area = goal_rect(home_platform)
    base_y = home_platform.top
    pole_x = area.right
    pygame.draw.line(screen, POLE, (pole_x, base_y), (pole_x, area.top), 6)
    flag = pygame.Rect(area.left, area.top, area.width, 28)
    pygame.draw.rect(screen, GOAL_RED, flag)
    label = font.render("HOME", True, WHITE)
    screen.blit(label, label.get_rect(center=flag.center))


# How long "You Win!" stays on screen before Level 1 starts again.
WIN_HOLD_FRAMES = FPS * 2


def new_game(player=None):
    """Level 1 with 3 lives. Nothing is saved between runs."""
    level_index = 0
    stage = build_level(level_index)
    if player is None:
        player = Player(*stage["start"])
    else:
        player.place(*stage["start"])
    return level_index, stage, player, STARTING_LIVES


def touched_hazard(player, clouds, other_planes):
    """True when the airplane's box overlaps a cloud or another airplane."""
    body = player_box(player)
    for cloud in clouds:
        if body.colliderect(cloud):
            return True
    for other in other_planes:
        if body.colliderect(other.rect()):
            return True
    return False


async def main():
    """Open the window and run the game until it is closed."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    # Bold Arial for headings. Regular Arial for instructions and the life count.
    # The flag uses a smaller Arial so HOME fits inside the red rectangle.
    display_font = pygame.font.SysFont("arial", 28, bold=True)
    title_font = pygame.font.SysFont("arial", 36, bold=True)
    body_font = pygame.font.SysFont("arial", 22)
    home_font = pygame.font.SysFont("arial", 16)

    rain = make_rain()
    level_index, stage, player, lives = new_game()
    won = False
    game_over = False
    win_frames = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                # Try the same level again. Do not send the player back to Level 1.
                stage = build_level(level_index)
                player.place(*stage["start"])
                lives = STARTING_LIVES
                game_over = False
            elif not game_over and not won:
                player.handle_event(event)

        level = stage["level"]
        if not game_over and not won:
            player.update(pygame.key.get_pressed(), stage["platforms"])
            for other in stage["planes"]:
                other.update()
            if level["rain"]:
                update_rain(rain)

            if player.fell or touched_hazard(player, stage["clouds"], stage["planes"]):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    player.place(*stage["start"])
            elif player_box(player).colliderect(goal_rect(stage["platforms"][-1])):
                if level_index < len(LEVELS) - 1:
                    level_index += 1
                    stage = build_level(level_index)
                    player.place(*stage["start"])
                    lives = STARTING_LIVES
                else:
                    won = True
                    win_frames = WIN_HOLD_FRAMES
        elif won:
            win_frames -= 1
            if win_frames <= 0:
                level_index, stage, player, lives = new_game(player)
                won = False
                game_over = False
                rain = make_rain()

        level = stage["level"]
        draw_background(screen, level)
        if level["rain"]:
            draw_rain(screen, rain)
        if stage["fog"]:
            screen.blit(stage["fog"], (0, 0))
        draw_platforms(screen, stage["platforms"], level)
        draw_goal(screen, home_font, stage["platforms"][-1])
        for cloud in stage["clouds"]:
            draw_cloud(screen, cloud)
        for other in stage["planes"]:
            other.draw(screen)
        player.draw(screen)

        ink = level["ink"]
        title = title_font.render(TITLE, True, ink)
        hint = body_font.render("Arrows or A/D to move. Space to jump.", True, ink)
        level_label = display_font.render(level["name"], True, ink)
        lives_label = body_font.render(f"Lives: {lives}", True, ink)
        # Lives and the level name share the top-left. The title sits to their
        # right, past the airplane that flies along the top of level 3.
        # The long instruction line, and any end-of-level message, sit along
        # the bottom, where no platform or hazard reaches.
        screen.blit(lives_label, (16, 4))
        screen.blit(level_label, (16, 40))
        screen.blit(title, (404, 4))
        screen.blit(hint, (408, 456))
        if won:
            message = title_font.render("You Win!", True, ink)
            screen.blit(message, (420, 492))
        if game_over:
            message = body_font.render("Level failed. Press R to try again.", True, ink)
            screen.blit(message, (420, 500))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
