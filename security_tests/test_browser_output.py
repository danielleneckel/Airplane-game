"""Checks the generated browser page for unsafe display of game data.

Pygame draws the level name and the life count as pictures. The page
does not insert those strings into HTML.
"""

from pathlib import Path

from settings import LEVELS

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "build" / "web" / "index.html").read_text()


def test_level_names_are_not_written_into_the_html_page():
    for level in LEVELS:
        assert level["name"] not in PAGE
        assert "<" not in level["name"]
        assert ">" not in level["name"]


def test_page_does_not_use_document_write_or_eval():
    assert "document.write" not in PAGE
    assert "eval(" not in PAGE


def test_innerhtml_helper_is_not_called_by_the_game():
    assert "innerHTML" in PAGE
    game = (ROOT / "main.py").read_text() + (ROOT / "player.py").read_text()
    assert "innerHTML" not in game
    assert "info_online(" not in game
    # The helper is defined, and the page does not call it on load.
    assert PAGE.count("info_online(") == 1


def test_displayed_game_text_is_passed_to_font_render():
    game = (ROOT / "main.py").read_text()
    assert 'f"Lives: {lives}"' in game
    assert "font.render" in game or "body_font.render" in game
    assert "innerHTML" not in game
