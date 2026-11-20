"""The cartoon airplane the player controls.

Movement, jumping, and gravity are unchanged. The nose tilt follows
vertical speed, and the airplane lands on floating platforms.
"""

import pygame

from settings import (
    GRAVITY,
    HEIGHT,
    JUMP_STRENGTH,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    TILT_EASE,
    TILT_MAX,
    WIDTH,
)

# Colors used only for the airplane picture.
# The outline keeps the white shape visible against the sky.
PLANE_WHITE = (255, 255, 255)
PLANE_OUTLINE = (0, 170, 255)
PLANE_WINDOW = (80, 200, 255)


class Player:
    """A small airplane that walks, jumps, and leans as it moves."""

    def __init__(self, x, y):
        # x and y are the center of the collision circle.
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        # True for the single frame when the airplane drops out of the window.
        self.fell = False
        # 1 faces right, -1 faces left.
        self.facing = 1
        # Degrees the nose is pointed up. Negative means the nose points down.
        self.tilt = 0.0
        self.image = self._build_sprite()

    def _build_sprite(self):
        """Draw one white airplane facing right.

        Moving left flips this same picture.
        """
        surface = pygame.Surface((120, 72), pygame.SRCALPHA)
        cx, cy = 60, 34

        def at(dx, dy):
            return (cx + dx, cy + dy)

        body = [at(-34, -6), at(16, -8), at(38, 0), at(16, 8), at(-34, 6)]
        tail = [at(-30, -4), at(-20, -20), at(-10, -4)]
        wing = [at(-2, 5), at(18, 4), at(10, 15), at(-12, 15)]

        pygame.draw.polygon(surface, PLANE_WHITE, wing)
        pygame.draw.polygon(surface, PLANE_OUTLINE, wing, 2)

        pygame.draw.polygon(surface, PLANE_WHITE, tail)
        pygame.draw.polygon(surface, PLANE_OUTLINE, tail, 2)

        pygame.draw.polygon(surface, PLANE_WHITE, body)
        pygame.draw.polygon(surface, PLANE_OUTLINE, body, 2)

        pygame.draw.circle(surface, PLANE_WINDOW, at(16, -2), 4)
        pygame.draw.circle(surface, PLANE_OUTLINE, at(16, -2), 4, 1)

        pygame.draw.circle(surface, PLANE_OUTLINE, at(0, 16), 4)
        pygame.draw.circle(surface, PLANE_WHITE, at(0, 16), 2)
        return surface

    def handle_event(self, event):
        """Jump once when Space is pressed and the airplane is standing on something."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.on_ground:
                self.vy = JUMP_STRENGTH
                self.on_ground = False

    def place(self, x, y):
        """Move the airplane to a safe spot and clear its speed and tilt."""
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.fell = False
        self.facing = 1
        self.tilt = 0.0

    def update(self, keys, platforms):
        """Move from the keyboard, then apply gravity, platforms, and nose tilt."""
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        self.vx = 0
        if left and not right:
            self.vx = -PLAYER_SPEED
            self.facing = -1
        elif right and not left:
            self.vx = PLAYER_SPEED
            self.facing = 1

        old_y = self.y
        self.fell = False
        # Positive vy moves down, because Pygame's y axis points downward.
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        # Keep the collision circle inside the left and right edges.
        if self.x < PLAYER_RADIUS:
            self.x = PLAYER_RADIUS
        if self.x > WIDTH - PLAYER_RADIUS:
            self.x = WIDTH - PLAYER_RADIUS

        # Land only when falling onto the top of a platform.
        # The previous bottom has to start above the top, so the airplane
        # can jump up past a platform and cannot fall through it.
        supported = False
        if self.vy >= 0:
            old_bottom = old_y + PLAYER_RADIUS
            bottom = self.y + PLAYER_RADIUS
            landed_on = None
            for platform in platforms:
                overlaps_x = (
                    self.x + PLAYER_RADIUS > platform.left
                    and self.x - PLAYER_RADIUS < platform.right
                )
                crossed_top = old_bottom <= platform.top + 1 and bottom >= platform.top
                # The smaller top value is the higher platform on the screen.
                if overlaps_x and crossed_top:
                    if landed_on is None or platform.top < landed_on.top:
                        landed_on = platform
            if landed_on is not None:
                self.y = landed_on.top - PLAYER_RADIUS
                self.vy = 0
                supported = True

        # The top, left, and right edges are solid.
        # The bottom is open: falling past it sets fell so the game can
        # take one life and respawn the airplane back at the start.
        if self.y < PLAYER_RADIUS:
            self.y = PLAYER_RADIUS
            if self.vy < 0:
                self.vy = 0
        if self.y + PLAYER_RADIUS > HEIGHT:
            self.fell = True

        self.on_ground = supported

        # Nose up while rising, level near the top, nose down while falling.
        # On a platform the target is level, then the angle eases toward it.
        if self.on_ground:
            target = 0
        else:
            target = max(-TILT_MAX, min(TILT_MAX, -self.vy))
        self.tilt += (target - self.tilt) * TILT_EASE

    def draw(self, screen):
        """Face the airplane left or right, then tilt it slightly."""
        picture = self.image
        if self.facing < 0:
            picture = pygame.transform.flip(self.image, True, False)

        # tilt is nose-up. Pygame rotates counter-clockwise, which lifts the right-hand nose.
        # Facing left flips the picture first, so the same positive tilt lifts that nose.
        angle = self.facing * self.tilt
        if abs(angle) > 0.4:
            picture = pygame.transform.rotate(picture, angle)

        screen.blit(picture, picture.get_rect(center=(int(self.x), int(self.y))))
