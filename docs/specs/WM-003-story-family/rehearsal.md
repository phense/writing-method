# Host routing rehearsal: story family

Run on 2026-11-13 on macOS with Claude Code 2.1.323 and Codex CLI 0.169.0, using
`scripts/run_host_evals.py` (Claude with `--native-auth`). The harness scores
which skills a host selects in one assessment turn. It does not read produced
text and does not see whether a request was declined.

## First run at `788fb4e`: twelve new cases per host

| Host | Passed | Failed (`unexpected_selection`) |
|---|---|---|
| Claude | 11 of 12 | `study-vault-draft-request` |
| Codex | 9 of 12 | `story-canon-review`, `story-voice-review`, `story-method-documentation` |

In all four failures the primary skill was the expected one. The failure was an
additional skill that the case prohibited.

| Case | What the host did | Disposition |
|---|---|---|
| `story-canon-review`, `story-voice-review` (Codex) | Opened `project-backlog` inside the story vault while looking for a recovery preamble; one run proposed initializing run state there | Defect. Every story skill now states that it has no recovery preamble and that a vault keeps no backlog or run directory. |
| `story-method-documentation` (Codex) | Read `story-bootstrap` as source material for the guide | Expectation was too strict. Only `story-drafting` and `story-voice-review` stay prohibited. Changed after seeing the result. |
| `study-vault-draft-request` (Claude) | Opened `story-drafting`, read its mode check and declined the draft | Expectation was wrong: that mode check is the designed mechanism. `story-drafting` is no longer prohibited. Changed after seeing the result. |

## Reruns

| Case | Host | Revision | Result |
|---|---|---|---|
| `story-canon-review` | Codex | `3a331b3` | 3 of 3 passed |
| `story-voice-review` | Codex | `3a331b3` | 3 of 3 passed |
| `story-method-documentation` | Codex | `3a331b3` | 3 of 3 passed |
| `study-vault-draft-request` | Claude | `3a331b3`, old expectation | 0 of 3 passed, same behaviour each time |
| `study-vault-draft-request` | Claude | `be08565`, corrected expectation | 2 of 2 passed |

No run selected a reader prose skill as primary for manuscript work, or a story
skill as primary for a README, release note, tutorial video or method guide.

## Regression: the nine earlier cases at `c68dbc1`

| Host | Passed | Failed (`unexpected_selection`) |
|---|---|---|
| Claude | 8 of 9 | `presentation-video-production` |
| Codex | 8 of 9 | `presentation-video-production` |

The documentation, PDF, tutorial-script, video-review and out-of-scope cases
passed on both hosts with the story family present. No story skill was selected
in any of the eighteen runs.

In the failing case both hosts chose `presentation-video-production` as primary
and additionally applied `documentation-authoring`, which the case prohibits.
The production skill itself sends the reader to the recovery preamble of
`documentation-authoring`. Neither that skill nor the case is changed by this
work.

Baseline comparison of that one case against release 0.3.0 (`29752ab`, without
the story family):

| Host | 0.3.0 | This branch |
|---|---|---|
| Codex | 0 of 1 passed | 0 of 1 passed |
| Claude | 2 of 3 passed | 0 of 3 passed |

On Codex the failure exists without the story family. On Claude the case is
unstable without it, and failed every time with it. Three runs per side do not
show whether this branch makes the case worse. The cause, a production skill
that requires a skill its routing case prohibits, belongs to WM-001 and is not
fixed here.

## Not covered

- The earlier cases ran once per host; apart from `presentation-video-production`
  no rate exists for them.
- Each case ran once per host in the first run; the reruns cover only the four
  failed cases. No five-run rate exists for the other cases.
- Leakage of one family's rules into produced text, a reply inside a vault and
  multi-turn sessions are not measurable with this harness.
- OpenCode was not exercised.
