# Regression testing

Date: 2026-11-19. No gameplay code was changed. Automated tests, a headless script, and a later manual browser playthrough are recorded separately below.

## What already exists

`security_tests/` has 27 pytest tests. They check security properties: bad values, the absence of a score, source text for level and life rules, the generated HTML page, configuration, and the `pythons.js` integrity hash.

They do not press keys, move the airplane, jump, run the game loop, or look at the screen.

Command and result:

`SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest security_tests -q`

27 passed, 0 failed, 0.11 seconds.

## Extra automated check

A one-time headless script called `Player.update`, `Player.handle_event`, `build_level`, `touched_hazard`, and `new_game` with a dummy display. It is not part of `security_tests/`, and it does not run `main()`.

Result: 25 passed, 0 failed.

That script confirmed right, left, A, and D movement, Space starting a jump only on the ground, landing on a platform, `fell` past the bottom, cloud overlap, three level names, a Level 3 goal overlap, `new_game()` returning Level 1 with 3 lives, and that the R-key branch still rebuilds the current level. It also rendered the words "You Win!", "Airplane Game", and "Above the Clouds" to an off-screen font image.

## Checklist

| Requirement | Automated result | Headless script | Manual play |
|---|---|---|---|
| Player movement | Not covered by the security suite. | Pass. Arrow keys and A/D moved the airplane. | Pass. Browser playthrough of all three levels. Gameplay worked. |
| Jumping | Not covered by the security suite. | Pass. Space jumps on the ground only, and the airplane moves up. | Pass. Included in the browser playthrough. Gameplay worked. |
| Collision detection | Not covered by the security suite. | Pass. Landing, falling off the bottom, and a cloud overlap. | Pass. Included in the browser playthrough. Gameplay worked. |
| Level 1 | Pass. Security test builds "Above the Clouds". | Pass. Same name, start is not the goal. | Pass. Played in the browser. Gameplay worked. |
| Level 2 | Pass. Security test builds "Sunset Flight". | Pass. Same name, start is not the goal. | Pass. Played in the browser. Gameplay worked. |
| Level 3 | Pass. Security test builds "The Storm". | Pass. Same name, start is not the goal. | Pass. Played in the browser. Gameplay worked. |
| Level transitions | Partial. Security tests read the source. The loop was not executed. | Not run as a live transition. | Pass. All three levels were played in order in the browser. |
| Winning | Partial. Source contains "You Win!" and the reset function. | Pass for `new_game()` only. The 2-second pause inside `main()` was not run. | Not specifically reported. The playthrough did not separately record the "You Win!" message or the automatic return to Level 1. |
| Losing | Partial. Security tests read the life rule. | The `fell` flag was set. A life was not removed by the game loop. | Not reported. Do not treat this as tested. |
| Restarting | Partial. The R-key code still rebuilds the current level. | That branch was read, not executed with a key press. | Not reported. Do not treat pressing R as tested. |
| Keyboard controls | Not covered by the security suite. | Pass for arrows, A, D, and Space on `Player` directly. R was not sent. | Pass for the controls used to play all three levels. R was not reported. |
| Visual elements | Not covered by the security suite. | Font images were drawn off screen for three strings. | Pass. The browser game was seen while all three levels were played, and gameplay worked. |
| Existing functionality | No failure in the security suite. | 25 passed, 0 failed. | Pass. All three levels and their gameplay worked in the browser. |
| Security tests | Pass. 27 passed, 0 failed. | Not applicable. | Not applicable. |

## Manual play

After the automated and headless checks, the browser game was opened and all three levels were played. All three levels and their gameplay worked correctly. Losing all lives and pressing R were not part of that report.

## Not specifically tested by hand

Losing all 3 lives, pressing R, and the "You Win!" pause were not reported from the manual session. The headless and source checks for those paths are still only automated.
