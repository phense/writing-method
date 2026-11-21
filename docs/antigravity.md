---
type: reference
audience: Authors and maintainers familiar with Antigravity and Git
version: 0.5.0
---
# Antigravity integration

Writing Method ships a native Antigravity plugin manifest at
`.antigravity-plugin/plugin.json` and bundles the shared
[Antigravity adapter](../shared/platform/antigravity.md) from Method Core.
It exposes all 30 writing, story, and shared support skills, and coexists
cleanly alongside [Engineering Method](https://github.com/phense/engineering-method).

## Install for Antigravity CLI, App, and IDE

Requires Python 3.11+, Git, and Antigravity (`agy`). Validate and install from
a local checkout or extracted release archive:

```sh
agy plugin validate --strict /absolute/path/to/writing-method
agy plugin install /absolute/path/to/writing-method
agy plugin list --json
```

Alternatively, install directly from GitHub:

```sh
agy plugin install https://github.com/phense/writing-method
```

Start a new Antigravity session after installing or updating so the refreshed
skill inventory is loaded.

## Install into a custom config directory or T3 Code

Hosts that launch `agy acp` with a separate `--gemini-dir` (such as T3 Code's
per-provider Antigravity directory) maintain their own `<gemini-dir>/config`
root rather than reading `~/.gemini/config/plugins/`. Use the bundled
ownership-checked installer to install or update a clean copy in any
Antigravity config directory:

```sh
python3 scripts/install-antigravity --check --config-dir /absolute/antigravity/config
python3 scripts/install-antigravity --config-dir /absolute/antigravity/config
```

The installer copies only clean plugin files (excluding `.git`, `dist`,
`__pycache__`, and local state), preserves script execute bits, and writes an
ownership marker so future updates or `--uninstall` calls never overwrite or
delete foreign or locally modified plugin directories. Existing `config.json`,
`mcp_config.json`, `hooks.json`, and other installed plugins remain untouched.

## Coexistence with Engineering Method

Both `writing-method` and `engineering-method` install into the same
`<config-dir>/plugins/` directory as independent plugins. When both are active,
use the invoking method's copy of shared support skills once rather than
running duplicate copies.

## Update and remove

For standalone Antigravity (`~/.gemini/config/plugins/`):

```sh
agy plugin uninstall writing-method
agy plugin install /absolute/path/to/writing-method
```

For installations managed by `scripts/install-antigravity`:

```sh
python3 scripts/install-antigravity --config-dir /absolute/antigravity/config
python3 scripts/install-antigravity --uninstall --check --config-dir /absolute/antigravity/config
python3 scripts/install-antigravity --uninstall --config-dir /absolute/antigravity/config
```

Uninstalling never removes documents, story vaults, `BACKLOG.md`, `FEATURES.md`,
or `.engineering-method/` state in target projects.

## Verification scope

Native validation (`agy plugin validate --strict`), isolated clean installation
(`agy plugin install` and `agy plugin list --json` in a disposable `HOME`),
and coexistence with Engineering Method were verified with `agy` 1.5.14 on macOS.
Discovery and manifest validation do not establish live model routing or prose
quality on Antigravity.
