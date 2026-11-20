# Before-and-after security assessment

Date: 2026-11-19. Sources: `security-review-findings.txt`, `remediation-report.txt`, `security-sri-baseline.txt`, and the current `build/web/index.html` line 1. No application code was changed for this report.

The security review confirmed one vulnerability, SR-01. The other reviewed areas did not produce a confirmed vulnerability, so they are not rows in this table.

| Area | Original | Security Issue | Remediation | Result |
|---|---|---|---|---|
| Remote script integrity (`pythons.js`) | External script loaded without integrity verification. | The browser could execute a modified external script. | Added the verified SHA-384 integrity hash and `crossorigin="anonymous"`. | Improved script integrity protection. |

## Conclusion

The page now checks `https://pygame-web.github.io/cdn/0.9.3/pythons.js` against `sha384-r9lBo2lFgr+vWZJnNU/iSR1gma5wmbPQS1gs+pGZ/ZMd2KcaKYZG/2bRGEBHD5z4` before running it. The script address did not change. Before the change, `security_tests/test_remote_runtime.py` failed because the tag had no integrity attribute (`security-sri-baseline.txt`). After the change, the security suite passed: 27 tests, 0 failed.

The hash protects that one file only. `pythons.js` still loads `main.js` and `main.wasm` from the same site with no integrity check. `build/web/index.html` line 288 still loads `browserfs.min.js`, and line 358 still loads `empty.html`, both without an integrity attribute. A later Pygbag build overwrites `index.html` and would remove this hash unless it is added again.

No other confirmed vulnerability was fixed because none was found. Input validation, XSS, injection, secrets, cookies, and authorization had no confirmed issue in this game. The local `http.server` banner, unpinned versions in `requirements.txt`, and the loose Content Security Policy were recorded as hardening notes, not as vulnerabilities, and they were left unchanged.
