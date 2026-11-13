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
At `c68dbc1` the production skill itself sent the reader to the recovery
preamble of `documentation-authoring`.

Baseline comparison of that one case against release 0.3.0 (`29752ab`, without
the story family):

| Host | 0.3.0 | This branch |
|---|---|---|
| Codex | 0 of 1 passed | 0 of 1 passed |
| Claude | 2 of 3 passed | 0 of 3 passed |

On Codex the failure exists without the story family. On Claude the case is
unstable without it, and failed every time with it. Three runs per side do not
show whether this branch makes the case worse. The cause, a production skill
that requires a skill its routing case prohibits, belongs to WM-001. It was removed
afterwards; see the full run below.

## Full run at `d583c74`: all 24 cases per host

Between the regression above and this run, `1d389c3` removed the delegation to
`documentation-authoring` from the three video skills, `2a450b2` added narrated
story videos with the cases `story-video-script` and `story-video-production`,
and `c9d0b21` added the case `story-listening-edition`. Every case ran once per
host.

| Host | Passed | Failed |
|---|---|---|
| Claude | 24 of 24 | none |
| Codex | 22 of 24 | `marketing-clip-out-of-scope`, `study-vault-draft-request` (both `unexpected_selection`) |

- `presentation-video-production` passed on both hosts. On Claude it had passed
  3 of 3 at `1d389c3`.
- `story-video-script` first failed on Claude with `missing_artifact`: the host
  chose `story-video-scripting` and wrote `decision.md` into the video project
  directory that the prompt named. The prompt now says where the record goes
  (`d583c74`); the case then passed on both hosts. Changed after seeing the
  result.
- The Codex run was interrupted after five cases because that prompt was edited
  while it ran; the harness stops when the plugin changes. The remaining
  nineteen cases ran one by one at `d583c74`.

The two Codex failures were repeated twice each at `6fda20d`:

| Case | Codex | What the host did |
|---|---|---|
| `marketing-clip-out-of-scope` | 1 of 3 passed | Routed to focused editing as expected. In the failing runs it opened `presentation-video-production` to read its exclusions and reported it as supporting, which the case prohibits. |
| `study-vault-draft-request` | 0 of 3 passed | Named `story-drafting` as primary, not `story-craft-research`. The run read in full recorded that the vault is `kind: study` and that drafting is not permitted. The harness scores the selection and cannot see the refusal. |

Neither expectation was changed. The first is an earlier case of the video
method; at `c68dbc1` it passed once on Codex. The second passed once on Codex
at `788fb4e`. Both are counted as failures.

## Unscripted requests (2026-11-13)

The harness tells a host to select a workflow. To see what happens without
that instruction, eleven plain German requests were sent once each to a host
with Writing Method and Engineering Method both loaded: no skill name, no
routing instruction, read-only tools. The probe is a script outside this
repository, not a harness, and one run per case is an observation, not a rate.

| Request | Expected skill | Claude | Codex |
|---|---|---|---|
| A failing test | `systematic-debugging` | loaded | loaded |
| A new feature across three modules | a specification skill | not loaded | loaded |
| An administrator guide | `documentation-authoring` | loaded | loaded |
| The difference between two Git commands | `explaining-concepts` | not loaded | loaded |
| Start a new story | `story-bootstrap` | loaded | loaded |
| "Write chapter 12" in a story vault | `story-drafting` | loaded | loaded |
| Does chapter 12 still fit what happened before | `story-canon-review` | loaded | loaded |
| Chapters no longer sound like the beginning | `story-voice-review` | loaded | loaded |
| An audiobook video of chapter 11, read as written | `story-video-scripting` | loaded | loaded |
| Two sentences changed for the audio version only | `story-video-scripting` | loaded | loaded |
| A tutorial video for new employees | `tutorial-video-scripting` | loaded | loaded |

Claude loaded the expected skill in 9 of 11 requests and Codex in 11 of 11. An
earlier Claude run ended each request with "tell me first how you will
proceed": the expected skill was then loaded in 4 of 11 requests and only
named in the plan in 4 more. A request for a plan lowers loading, not the
choice. Claude ran from the working tree, Codex from the installed plugin copy
of the same revision.

## Corrections and measured runs after release 0.4.0 (2026-11-13)

**Routing harness, Codex.** Two corrections at `c193988`: the instruction file of a study vault names `story-craft-research` as the skill for every request, and `presentation-video-production` states that filmed material, marketing clips and short-form video are outside the video method. Both cases then passed 3 of 3 on Codex (`marketing-clip-out-of-scope` before: 1 of 3; `study-vault-draft-request` before: 0 of 3). The fixture of the study-vault case received the same sentence as the vault template, after the result was known.

**Earlier Codex timeouts.** The runs that ended with `timeout` and no event had a cause in the harness: the host inherited an open standard input and waited for more input. Method Core `5d8519b` closes it.

**Unscripted requests, measured.** The probe became `scripts/run_natural_evals.py` (Method Core). Nine cases of this plugin under `evals/natural/` and three of Engineering Method ran three times per host with both plugins loaded, the hosts' coordinator models (`fable`, `gpt-6-astra`), and on Codex the plugins as installed. A hit is a run in which an expected skill was loaded and no prohibited one.

| Request | Expected | Claude | Codex |
|---|---|---|---|
| An administrator guide | `documentation-authoring` or `writing-procedures` | 3 of 3 | 3 of 3 |
| The difference between two Git commands | `explaining-concepts` | 1 of 3 | 3 of 3 |
| Start a new story | `story-bootstrap` | 3 of 3 | 3 of 3 |
| "Write chapter 12" in a story vault | `story-drafting` | 3 of 3 | 3 of 3 |
| Does chapter 12 still fit what happened before | `story-canon-review` | 3 of 3 | 3 of 3 |
| Chapters no longer sound like the beginning | `story-voice-review` | 3 of 3 | 3 of 3 |
| An audiobook video of chapter 11, read as written | `story-video-scripting` | 3 of 3 | 3 of 3 |
| Two sentences changed for the audio version only | `story-video-scripting` | 3 of 3 | 3 of 3 |
| A tutorial video for new employees | `tutorial-video-scripting` | 3 of 3 | 3 of 3 |
| A failing test (Engineering Method) | `systematic-debugging` | 2 of 3 | 3 of 3 |
| A feature across three modules (Engineering Method) | a specification skill | 3 of 3 | 3 of 3 |
| A typing error in a README (Engineering Method) | no skill | 3 of 3 | 2 of 3 |

Totals: Claude 33 of 36 runs, Codex 35 of 36. Three things were changed after seeing results and are part of these figures:

- The guide case first expected `documentation-authoring` only. Claude loaded `writing-procedures` in all three runs, which is a correct skill for a how-to; the expectation now accepts either.
- The Codex figures are a re-scoring of the saved transcripts. The runner first counted a skill read only when the command was a plain `cat`; Codex reads skills inside compound commands. Eight runs scored as misses contained a complete read of the expected skill (27 of 36 before, 35 of 36 after; Method Core `64d9a02`).
- A first measurement used the routing-role models and, on Codex, repository skill links. It was discarded: the smaller Claude model loaded skills far less often, and Codex looked for paths that did not exist.

After the measurement the description of `explaining-concepts` was widened to name short questions such as what something is or how two things differ. The concept question then loaded the skill in 3 of 3 runs on Claude (`1d9c3f0`; before: 1 of 3). No other description was changed.

Three runs per case show a tendency, not a rate, and nothing here reads the produced text.

## Not covered

- The earlier cases ran once per host; apart from `presentation-video-production`
  no rate exists for them.
- Each case ran once per host in the first run; the reruns cover only the four
  failed cases. No five-run rate exists for the other cases.
- Leakage of one family's rules into produced text, a reply inside a vault and
  multi-turn sessions are not measurable with this harness.
- The unscripted requests ran once per host; they show no rate and read no
  produced text.
- OpenCode was not exercised.
