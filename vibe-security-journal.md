# Vibe security journal

Airplane Game, 2026-11-19. These notes are from the security assignment. Cursor inspected the project files. I checked its answers against those files and the saved test output before accepting them.

## 1. Initial security review and baseline

1. Security objective
Find real security problems in the Python game and the browser page in `build/web/`.

2. Prompt
"Act as a senior application security engineer conducting a comprehensive security assessment of my Airplane Game project. ... Do not modify, delete, or rewrite any files. This is an investigation only."

3. AI assessment
Cursor read `main.py`, `player.py`, `settings.py`, `requirements.txt`, `pygbag.ini`, and `build/web/index.html`. It reported one confirmed issue: line 1 loads `pythons.js` from `pygame-web.github.io` with no integrity check (SR-01, Medium). It said input validation, XSS, injection, secrets, cookies, and authorization were not confirmed problems because the game has no backend and no player-supplied HTML.

4. Your assessment
Cursor's summary needed a check against the files. `security-review-findings.txt` matches that review: one confirmed Medium finding, two false positives, and three hardening notes that are not vulnerabilities. I did not treat every warning as a bug.

5. Action
No application code was changed. The findings were saved in `security-review-findings.txt`.

6. Verification
The script tag on line 1 of `build/web/index.html` was the original evidence. Later, `security-sri-baseline.txt` showed the same tag with no `integrity` attribute.

7. Result
The baseline is one confirmed issue, SR-01. The game files themselves did not show a confirmed injection, XSS, secret, or login bug.

## 2. External script and SRI analysis

1. Security objective
Decide whether Subresource Integrity can be added to `pythons.js` without breaking the game, and whether that protects every file the page loads.

2. Prompt
"I want to investigate the security risk of loading pythons.js from pygame-web.github.io without an integrity check. ... Do not invent an integrity hash. Only use a verified hash of the exact resource. ... Do not make any remediation changes until you explain the proposed solution to me."

3. AI assessment
Cursor downloaded `https://pygame-web.github.io/cdn/0.9.3/pythons.js` (69,205 bytes) and computed SHA-384 `sha384-r9lBo2lFgr+vWZJnNU/iSR1gma5wmbPQS1gs+pGZ/ZMd2KcaKYZG/2bRGEBHD5z4`. It said the file then loads more scripts, including `main.js` and `main.wasm`, with no hashes. It recommended adding the hash and `crossorigin="anonymous"` to the existing tag only.

4. Your assessment
The hash had to come from the downloaded file, not from a guess. The saved baseline test failed on the original tag, which confirms the attribute was missing. The limit is also real: line 288 still loads `browserfs.min.js` and line 358 still loads `empty.html` with no integrity attribute.

5. Action
A checkpoint archive was saved as `checkpoint-pre-sri-2026-11-19.tar.gz`. `security_tests/test_remote_runtime.py` was added. `index.html` was not changed yet.

6. Verification
`security-sri-baseline.txt`: `test_remote_pythons_runtime_has_integrity_check` failed. The tag in the failure has the remote `src` and no `integrity` attribute.

7. Result
SRI is possible for the first script. It does not cover the files that script loads afterward. The failing test is the before-fix evidence.

## 3. SRI remediation

1. Security objective
Add the verified hash so the browser will not run a changed `pythons.js`.

2. Prompt
"Apply the remediation for SR-01. ... Use the verified SHA-384 hash ... Add the integrity attribute to the existing pythons.js script tag. Add crossorigin=\"anonymous\". Do not change the script URL. ... Do not rebuild Pygbag unless necessary."

3. AI assessment
Cursor added only those two attributes on line 1 of `build/web/index.html`. It left the URL the same and did not edit `main.py`, `player.py`, or `settings.py`. It did not rebuild the page with Pygbag.

4. Your assessment
I compared line 1 with the hash from the earlier download. They match, and `crossorigin="anonymous"` is present. Cursor was right that this is a one-file fix. It does not make the rest of the CDN files safe.

5. Action
The script tag was updated. Nothing else in the game rules was changed for this fix.

6. Verification
`security-test-report-after-fix.txt` shows the SRI test passed and the original 26 security tests passed. The page was reloaded at `http://127.0.0.1:8001/`. The browser accepted the hash and continued to `main.js` and `main.wasm`. That reload checked the script load. The three-level browser playthrough is in entry 5.

7. Result
`pythons.js` is now checked before it runs. Later remote files are still unchecked.

## 4. Automated security testing

1. Security objective
Scan the Python game with Bandit and add tests for the security areas that apply to this project.

2. Prompt
"Complete Part 12: Automated Security Testing. ... Choose and use Bandit ... to scan main.py, player.py, and settings.py. ... Do not treat every warning as a vulnerability."
A later prompt asked for a pytest suite in `security_tests/` covering input, game state, errors, browser output, and configuration.

3. AI assessment
Bandit 1.9.4 reported four low findings, all B311, on `random` in `main.py` lines 119 and 173. Cursor called that a false positive because the calls only place rain. It then added pytest tests. The first run of those tests was 26 passed, recorded in `security-test-results.txt`.

4. Your assessment
I agree the rain warning is not a vulnerability. `random` is not used for a password or a token. The pytest tests check the functions and the HTML file. They do not play the game. Cursor's "26 passed" matches `security-test-results.txt`. The browser playthrough is recorded in entry 5.

5. Action
Bandit was installed in the virtual environment. The rain code was not changed. The tests were saved under `security_tests/`. The SRI test was added later, so the suite became 27 tests.

6. Verification
`bandit-report.txt` shows 4 low, 0 medium, 0 high. `security-test-results.txt` shows 26 passed. After the SRI test and the hash were in place, a later run recorded 27 passed.

7. Result
The only Bandit result is a false positive. The pytest suite passes and guards the SRI line. It is a separate result from the headless checks and from the browser playthrough.

## 5. Regression testing and gameplay functionality

1. Security objective
See whether the security edits and the Level 3 restart change broke movement, jumping, collisions, levels, winning, losing, or the keyboard controls.

2. Prompt
"Complete Part 15: Regression Testing. ... Do not claim that manual gameplay tests were completed. Clearly distinguish automated tests from manual tests. Do not change gameplay code unless a genuine regression is discovered."

3. AI assessment
Cursor said the 27 security tests do not move the airplane or run `main()`. It ran a separate headless script against `Player` and the level functions. That script reported 25 passed and 0 failed. Cursor did not change gameplay code.

4. Your assessment
The headless results only cover those function calls. After that script, I opened the browser game and played all three levels. All three levels and their gameplay worked correctly. I did not specifically test losing all lives or pressing R.

5. Action
No gameplay code was changed. The checklist was saved in `regression-testing.md` and then updated with the manual playthrough.

6. Verification
Automated: 27 passed, 0 failed, 0.11 seconds. Headless: 25 passed, 0 failed. Manual: browser playthrough of Levels 1, 2, and 3. Gameplay worked. Losing and R were not reported.

7. Result
No regression was found in the automated checks or in the three-level browser playthrough. Losing and the R restart were not part of the manual test.
