# Finding SEC-01: Missing Subresource Integrity for External Script

Severity: Medium

Location: build/web/index.html, line 1.

## Description

`pythons.js` was loaded from `https://pygame-web.github.io/cdn/0.9.3/pythons.js` with no integrity verification. The browser downloaded that file and ran it. The address included version 0.9.3, but nothing checked that the bytes still matched the file reviewed for this project.

## Security impact

If that file were replaced, the browser could execute the modified script in the game page. The script could change the page, read keys pressed in the game, and load more code. This game has no accounts and no saved scores, so the effect stays in that browser tab. It does not reach the rest of the computer. The risk depends on someone changing the file on `pygame-web.github.io`.

## Root cause

Pygbag 0.9.3 writes this script tag from its page template. The template sets the `src` and does not add an `integrity` attribute. The generated page was used as produced, so line 1 had no hash.

## Evidence

`security-sri-baseline.txt` records the check against the original page. `security_tests/test_remote_runtime.py::test_remote_pythons_runtime_has_integrity_check` failed. The tag it found was:

`<script src="https://pygame-web.github.io/cdn/0.9.3/pythons.js" type=module id="site" ... async defer>`

That tag had no `integrity` attribute.

## AI assistance

Cursor read `build/web/index.html`, found the script tag on line 1, and downloaded the file at that address. The download was 69,205 bytes and contained no integrity checks of its own. Cursor computed the SHA-384 hash from those bytes and showed that the page would run the file without comparing it to a hash.

## Remediation

The same script tag now includes the verified hash and `crossorigin="anonymous"`. The URL was not changed.

`integrity="sha384-r9lBo2lFgr+vWZJnNU/iSR1gma5wmbPQS1gs+pGZ/ZMd2KcaKYZG/2bRGEBHD5z4"`

## Verification

After the change, `test_remote_pythons_runtime_has_integrity_check` passed. The full `security_tests` suite was run again: 27 passed, 0 failed. The current line 1 of `build/web/index.html` still contains that hash and `crossorigin="anonymous"`.

The hash covers `pythons.js` only. Files loaded afterward, including `main.js` and `main.wasm`, still have no integrity check.

## Regression impact

`regression-testing.md` keeps the three checks separate.

Automated: the 27 security tests passed.

Headless: a script checked movement, jumping, landing, a hazard overlap, the three level names, and the Level 1 reset function. It reported 25 passed and 0 failed. It did not run the game window.

Manual: after those checks, the browser game was opened and all three levels were played. All three levels and their gameplay worked correctly. That session did not report losing all lives or pressing R.
