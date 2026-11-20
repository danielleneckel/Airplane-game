"""Regression check for the remote Pygbag runtime.

This records whether build/web/index.html pins pythons.js with
Subresource Integrity. The hash below was computed on 2026-11-19 from
the 69,205-byte file at
https://pygame-web.github.io/cdn/0.9.3/pythons.js
using SHA-384. It was not guessed.

SRI on this one tag does not cover scripts that pythons.js loads later.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "build" / "web" / "index.html"

RUNTIME_URL = "https://pygame-web.github.io/cdn/0.9.3/pythons.js"
# Verified SHA-384 of the downloaded file, 69205 bytes, last-modified 2026-03-17.
VERIFIED_INTEGRITY = "sha384-r9lBo2lFgr+vWZJnNU/iSR1gma5wmbPQS1gs+pGZ/ZMd2KcaKYZG/2bRGEBHD5z4"


def _runtime_tag():
    text = PAGE.read_text()
    match = re.search(
        r"<script\b[^>]*\bsrc=\"" + re.escape(RUNTIME_URL) + r"\"[^>]*>",
        text,
    )
    assert match, "index.html does not load " + RUNTIME_URL
    return match.group(0)


def test_remote_pythons_runtime_has_integrity_check():
    tag = _runtime_tag()
    assert f'integrity="{VERIFIED_INTEGRITY}"' in tag
    assert 'crossorigin="anonymous"' in tag
