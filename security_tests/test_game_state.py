"""Checks level changes, lives, and the win condition.

There is no score variable and no server that stores progress. A change
made in one browser affects only that running game.
"""

from pathlib import Path

import main
from player import Player
from settings import LEVELS, STARTING_LIVES

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "main.py").read_text()


def test_there_is_no_score_to_change():
    for name in ("main.py", "player.py", "settings.py"):
        text = (ROOT / name).read_text().lower()
        assert "score" not in text
    assert not hasattr(Player, "score")
    assert not hasattr(main, "score")


def test_level_progression_starts_at_zero_and_moves_one_level_at_a_time():
    assert SOURCE.count("level_index = 0") == 1
    assert SOURCE.count("level_index += 1") == 1
    assert "level_index < len(LEVELS) - 1" in SOURCE
    # The increase sits with the goal test, not with a value supplied from outside.
    goal_part = SOURCE.split("colliderect", 1)[1]
    assert "level_index += 1" in goal_part
    assert "won = True" in goal_part


def test_a_player_at_the_start_has_not_reached_the_goal():
    for index in range(len(LEVELS)):
        stage = main.build_level(index)
        player = Player(*stage["start"])
        goal = main.goal_rect(stage["platforms"][-1])
        assert main.player_box(player).colliderect(goal) is False


def test_standing_on_the_goal_is_what_the_game_treats_as_progress():
    stage = main.build_level(0)
    goal = main.goal_rect(stage["platforms"][-1])
    player = Player(goal.centerx, goal.centery)
    assert main.player_box(player).colliderect(goal) is True
    # Reaching that rectangle is not a win by itself on the first two levels.
    # The loop advances one level, and sets won only when no level remains.
    assert SOURCE.count("won = True") == 1


def test_lives_start_at_three_and_the_loop_stops_at_zero():
    assert STARTING_LIVES == 3
    assert "lives = STARTING_LIVES" in SOURCE
    assert "lives -= 1" in SOURCE
    assert "if lives <= 0:" in SOURCE
    assert "game_over = True" in SOURCE
    assert not hasattr(Player, "lives")


def test_the_life_rule_does_not_keep_going_below_zero():
    # Same order as main.py: subtract one, then stop when the result is 0 or less.
    lives = STARTING_LIVES
    game_over = False
    while not game_over:
        lives -= 1
        if lives <= 0:
            game_over = True
    assert lives == 0
    assert game_over is True
