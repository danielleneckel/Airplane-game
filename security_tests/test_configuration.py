"""Checks the settings that ship with this project.

The local file server is not a public website. These tests look for
debug switches that turn on by themselves and for secrets in the files
a player can open.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "build" / "web" / "index.html").read_text()


def test_debug_panel_starts_hidden_and_is_not_called_on_load():
    assert "gui_debug : 2" in PAGE
    assert '<div id="system" hidden>' in PAGE
    assert "function debug()" in PAGE
    # custom_onload(false) would show the panel. It appears only inside debug().
    debug_body = PAGE.split("function debug()", 1)[1].split("function info_inline", 1)[0]
    assert "custom_onload(false)" in debug_body
    assert PAGE.count("custom_onload(false)") == 1


def test_hidden_frame_does_not_request_camera_microphone_or_location():
    allow = PAGE.split('allow="', 1)[1].split('"', 1)[0]
    assert allow == "autoplay; fullscreen"
    assert "camera" not in allow
    assert "microphone" not in allow
    assert "geolocation" not in allow


def test_page_has_a_content_security_policy():
    assert 'http-equiv="Content-Security-Policy"' in PAGE


def test_project_files_do_not_contain_secrets_or_this_computers_home_folder():
    checked = [
        ROOT / "main.py",
        ROOT / "player.py",
        ROOT / "settings.py",
        ROOT / "requirements.txt",
        ROOT / "pygbag.ini",
        ROOT / "build" / "web" / "index.html",
    ]
    secret_words = ("api_key", "secret_key", "BEGIN PRIVATE KEY", "password =")
    for path in checked:
        text = path.read_text().lower()
        assert "/users/" not in text
        for word in secret_words:
            assert word not in text


def test_requirements_list_only_the_game_packages():
    requirements = (ROOT / "requirements.txt").read_text()
    assert "pygame" in requirements
    assert "pygbag" in requirements
    assert "flask" not in requirements.lower()
    assert "django" not in requirements.lower()
