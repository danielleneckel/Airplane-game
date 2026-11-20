"""Checks that bad values raise ordinary Python errors.

The messages should name the problem, not a password, a token, or a
folder on this computer.
"""

import pytest

import main
from player import Player


def test_wrong_platform_data_raises_without_sensitive_text():
    with pytest.raises(ValueError) as exc:
        main.make_platforms([("not", "numbers")])
    message = str(exc.value)
    assert "password" not in message.lower()
    assert "Users" not in message
    assert "token" not in message.lower()


def test_invalid_player_position_raises_a_plain_type_error():
    class NoKeys:
        def __getitem__(self, key):
            return False

    player = Player("home", None)
    with pytest.raises(TypeError) as exc:
        player.update(NoKeys(), [])
    assert "Users" not in str(exc.value)


def test_hazard_check_rejects_a_missing_player_without_a_path():
    with pytest.raises(AttributeError) as exc:
        main.touched_hazard(None, [], [])
    assert "Users" not in str(exc.value)


def test_rain_update_rejects_a_drop_that_is_not_a_list():
    with pytest.raises(TypeError) as exc:
        main.update_rain(["not a drop"])
    assert "Users" not in str(exc.value)
