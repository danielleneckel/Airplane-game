"""Checks for values the game functions actually accept.

The game has no text box, query string, or posted form. These tests call
the functions the game loop uses and record what unexpected values do.
"""

from pathlib import Path

import pytest

import main
from player import Player
from settings import HEIGHT, LEVELS, PLAYER_RADIUS, WIDTH

ROOT = Path(__file__).resolve().parents[1]


class PressedKeys:
    """A stand-in for pygame.key.get_pressed(). Missing keys are not pressed."""

    def __init__(self, pressed=()):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed


def test_valid_level_indexes_build_the_three_levels_in_order():
    names = [main.build_level(index)["level"]["name"] for index in range(len(LEVELS))]
    assert names == ["Above the Clouds", "Sunset Flight", "The Storm"]


def test_missing_level_index_is_rejected():
    with pytest.raises(TypeError) as exc:
        main.build_level()
    assert "Users" not in str(exc.value)


def test_empty_and_text_level_indexes_are_rejected():
    for bad in ("", "1", None):
        with pytest.raises(TypeError) as exc:
            main.build_level(bad)
        assert "Users" not in str(exc.value)


def test_negative_level_index_is_not_read_from_the_player():
    # Python lists treat -1 as the last item. The game loop never does that.
    # It starts at 0 and adds 1 only after the airplane reaches the goal.
    source = (ROOT / "main.py").read_text()
    assert "input(" not in source
    assert "level_index = 0" in source
    assert "level_index += 1" in source
    assert main.build_level(-1)["level"]["name"] == LEVELS[-1]["name"]


def test_huge_level_index_raises_without_a_file_path():
    with pytest.raises(IndexError) as exc:
        main.build_level(10**9)
    message = str(exc.value)
    assert message == "list index out of range"
    assert "Users" not in message


def test_player_coordinates_are_clamped_to_the_screen():
    stage = main.build_level(0)
    platforms = stage["platforms"]

    left = Player(-10**9, 200)
    left.update(PressedKeys(), platforms)
    assert left.x == PLAYER_RADIUS

    right = Player(10**9, 200)
    right.update(PressedKeys(), platforms)
    assert right.x == WIDTH - PLAYER_RADIUS

    high = Player(200, -10**9)
    high.update(PressedKeys(), platforms)
    assert high.y == PLAYER_RADIUS

    low = Player(200, HEIGHT * 10)
    low.update(PressedKeys(), platforms)
    assert low.fell is True


def test_unexpected_keyboard_object_does_not_reveal_a_path():
    player = Player(100, 100)
    with pytest.raises(TypeError) as exc:
        player.update(None, [])
    assert "Users" not in str(exc.value)
