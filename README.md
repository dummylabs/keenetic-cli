# keenetic-cli

A command-line tool for inspecting and managing a **Keenetic router** through its HTTP API (RCI),
plus an agent skill that teaches an AI coding assistant how to drive it safely.

It exists because letting an agent talk to a router with raw `curl` is a bad idea. Keenetic's API
reports command failures inside HTTP 200 bodies, hands out secrets in plain reads, and makes
`reboot` look exactly like a query. This CLI handles authentication, redacts credentials from every
output, and refuses anything that could change the router unless you say so explicitly.

Single file, no packaging: dependencies are declared inline per [PEP 723](https://peps.python.org/pep-0723/),
so `uv run` fetches them itself. The only third-party dependency is `aiohttp`.

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)
- A Keenetic router reachable over HTTP, and an account on it with the **Web interface** permission

## Install

```bash
git clone https://github.com/dummylabs/keenetic-cli.git
cd keenetic-cli
cp .env.example .env
```

Fill in `KEENETIC_HOST` and `KEENETIC_USERNAME` in `.env`.

### The router account

Create a dedicated user on the router rather than reusing the admin account. In the web interface:
**Management → Users → add user**.

Tick **Web interface** — that permission alone is enough for everything this tool does, including
writes. **Command line** (telnet/SSH) is not needed; leaving it off means the account cannot get a
shell on the router at all.

Do **not** tick **Prohibit saving system settings** if you want `set policy` to work: on Keenetic,
write access is the default state and that checkbox takes it away.

> Note: some Keenetic firmware rejects a hyphen in the username. `keenetic_cli` works.

### The password

The password does not go in `.env`. On macOS it lives in the keychain:

```bash
security add-generic-password -U -s keenetic -a <router-username> -w
```

Pass `-w` with **no value** so `security` prompts for the password instead of taking it as a
command-line argument, where the process list can see it.

The keychain item is keyed by the *router* username, so pointing `--env-file` at a second router
looks up that router's own password instead of silently reusing this one's.

If you are not on macOS, or the keychain is unavailable, set `KEENETIC_PASSWORD` in `.env` or in the
environment — that path still works and takes precedence. It is deliberately kept as an escape
hatch: this is a tool for diagnosing a broken network, so it must not require working infrastructure
to start.

## Usage

### Clients and policies

```bash
uv run keenetic_cli.py list clients                    # active clients
uv run keenetic_cli.py list clients --include-inactive
uv run keenetic_cli.py list policies
```

```bash
uv run keenetic_cli.py set policy --mac aa:bb:cc:dd:ee:ff --policy default
uv run keenetic_cli.py set policy --name my-laptop --policy Policy0
```

`--mac` and `--name` are mutually exclusive and one is required. `--policy` accepts `default`,
`not_internet`, a policy id, or a policy's exact description.

A policy change is confirmed by reading the state back, because the router reports failure inside a
success response. The result also says whether the change was **persisted** — if the batched
`system configuration save` failed, the policy is live but will not survive a reboot, and that is
reported separately rather than as a rejected write.

### Interfaces

```bash
uv run keenetic_cli.py show interfaces
uv run keenetic_cli.py show interfaces --connected
uv run keenetic_cli.py show interfaces --type wireguard
uv run keenetic_cli.py show interfaces --name Wireguard0 --json
uv run keenetic_cli.py show interface-stat --name Wireguard0
```

### Logs

```bash
uv run keenetic_cli.py show log
uv run keenetic_cli.py show log --since-minutes 30 --errors
uv run keenetic_cli.py show log --lines 500 --grep wireguard
uv run keenetic_cli.py show log --since "2026-01-31 13:00:00"
```

`--errors` shows `Error`/`Critical`/`Fatal` entries plus problem-shaped network messages such as
`timeout`, `failed`, `did not complete`, `stopped hearing back` and `retrying handshake`.

### Free IP addresses

```bash
uv run keenetic_cli.py show dhcp
uv run keenetic_cli.py show dhcp --occupied
uv run keenetic_cli.py show dhcp --json
```

Reports the DHCP pool bounds, what is occupied (reservations, active leases, and hosts merely seen
at an address), and **two** lists of free addresses.

Two lists, not one, because they are different claims. Only an address **outside the pool** is safe
to configure statically on a device; one inside the pool is free this second and the router may
lease it to the next machine that asks.

Occupancy is counted from two sources: `/rci/show/ip/dhcp/bindings` does not know about an address
configured on the device itself, and the hotspot registry does not know about a reservation for a
host that is currently offline.

### Raw API calls

```bash
uv run keenetic_cli.py api request --method GET --endpoint /rci/show/interface
```

Any body-less `GET` on a non-action path is allowed by default. Per the RCI specification, GET
retrieves settings and does not execute commands, so config reads outside `/rci/show/...` — for
example `/rci/ip/policy` — need no flag.

`--unsafe` is required for `POST`/`DELETE`/`PUT`, and for `GET` on an action path (`save`, `reboot`,
`reset`, `erase`, `upgrade`, and others):

```bash
uv run keenetic_cli.py api request \
  --method POST \
  --endpoint /rci/ \
  --data-json '[{"show":{"interface":{}}}]' \
  --unsafe
```

JSON output redacts sensitive fields by default. `--no-redact` prints the router's response
unmasked.

## Safety model

The gate that decides whether a request needs `--unsafe` is the most safety-critical code here. A
request is allowed without the flag only when all three hold:

1. the method is `GET`;
2. no path segment **and no query parameter name** names an action — the RCI query string is an
   argument channel, so `/rci/system/configuration?save` is the same action as `.../save`;
3. there is no request body, since a nested command sent as a `GET` body would be invisible to (2).

Segments are matched after percent-decoding, case folding, and stripping control characters,
surrounding whitespace and dots, so `/rci/system/configuration/%73ave` does not slip through.

One check is **not** waived by `--unsafe`, because it is about which machine is contacted rather
than what runs there: the endpoint must be a path rooted at a single `/`. Otherwise
`@evil.example/rci/show/version` would turn the router's `host:port` into URL userinfo and send the
request, and any `--data-json` body, somewhere else entirely.

Redaction applies to every request, read-only or not, and to every output mode equally — a table is
never a way around what `--json` masks.

## The agent skill

`skill/` contains a skill that teaches an agent to use this CLI: the safety rules, the command
recipes, and how to translate Keenetic CLI commands into `/rci/...` endpoints.

For Claude Code:

```bash
cp -r skill ~/.claude/skills/keenetic-router-api
```

Then edit `~/.claude/skills/keenetic-router-api/SKILL.md` and replace `/path/to/keenetic-cli` with
wherever you cloned this repository.

The skill deliberately does not bundle Keenetic's command reference — that is the vendor's
copyrighted manual, not ours to redistribute. Get the CLI manual for your model from Keenetic's
documentation site; the skill explains where to point the agent at it if you convert it to Markdown.

## Tests

```bash
uv run tests/test_keenetic_cli.py
```

93 offline tests: no router, no network, no pytest. They cover the pure, safety-relevant logic —
the unsafe-request gate, redaction, log parsing, DHCP arithmetic, and config resolution. Everything
beyond that needs a live router, so try read-only commands first.

## License

MIT — see [LICENSE](LICENSE).

This project is not affiliated with or endorsed by Keenetic.
