# keenetic-cli

A command-line tool for inspecting and managing a **Keenetic/Netcraze router** through its HTTP API (RCI), plus an agent skill that teaches an AI coding assistant how to drive it safely.

It exists because letting an agent talk to a router with raw `curl` is a bad idea. Keenetic/Netcraze's API reports command failures inside HTTP 200 bodies, hands out secrets in plain reads, and makes `reboot` look exactly like a query. This CLI handles authentication, redacts credentials from every output, and refuses anything that could change the router unless you say so explicitly.

Single file, no packaging: dependencies are declared inline per [PEP 723](https://peps.python.org/pep-0723/), so `uv run` fetches them itself. The only third-party dependency is `aiohttp`.

## What you can ask the agent to do

With the skill installed, you stop clicking through the router's web interface and just ask:

- *"Which devices are routed through the Netherlands VPN right now?"*
- *"Put the kids' tablet back on the default policy."*
- *"What routing policies do I even have?"*
- *"Is the printer online, and what IP did it get?"*
- *"Anything wrong in the router log in the last hour?"*
- *"Did anything complain about WireGuard today?"*
- *"Are all my tunnels up? Which one keeps dropping?"*
- *"How much traffic went through the VPN interface?"*
- *"I'm adding a NAS — find me a free IP that DHCP won't hand out to anything else."*
- *"Which addresses are reserved, and which are just leased right now?"*
- *"Change the DNS servers the router hands out over DHCP."*
- *"Add a static route for this subnet through the VPN interface."*
- *"Set up a new WireGuard peer."*
- *"Forward this port to my server."*
- *"Reserve this IP for that device permanently."*
- *"What does the router think its WAN configuration is?"*
- *"Turn SSH on."*
- *"Schedule the guest network to switch off overnight."*

Some of those only read the router; others change it, and the ones that change it need your say-so — see [Safety model](#safety-model).

## Safety model

Handing a router to an AI agent raises two obvious worries. Both were design constraints here, not afterthoughts.

### Your secrets do not reach the conversation

Everything this tool prints passes through redaction first, so router credentials do not end up in a chat transcript, in a log an agent writes, or in a bug report someone pastes online.

That covers more than the obvious `password` field. The router hands out secrets in several shapes, and each is caught: JSON keys containing `password`, `secret`, `token`, `psk` or ending in `-key`; free-text directives in `show running-config`, where the keyword is not at the start of the line (`wireguard private-key <key>`, `authentication wpa-psk ns3 <psk>`); and the oddly-named ones that match no general rule — `servicepass`, `wlankey`, `wlanwps` in `show defaults`, `authtoken` for NextDNS, the WPS PIN, the SIM PIN, RADIUS secrets.

Redaction applies to every command and every output mode equally, read-only or not. A table is never a way around what `--json` masks. `--no-redact` exists for when you genuinely need the raw value, and it is the only way to get one.

Your own router password gets the same treatment from the other direction: it never travels in the clear and never appears in the tool's own output. Authentication hashes it into a challenge response, and the config object that holds it is built so that printing it while debugging cannot leak it.

What is *not* hidden is the inventory itself — device names, MAC addresses, IP assignments. Showing you those is the job, so a conversation about your network will contain your network. Redaction is about credentials, not about the existence of a printer.

### Nothing changes the router by accident

The gate that decides whether a request needs `--unsafe` is the most safety-critical code here. A request is allowed without the flag only when all three hold:

1. the method is `GET`;
2. no path segment **and no query parameter name** names an action — the RCI query string is an argument channel, so `/rci/system/configuration?save` is the same action as `.../save`;
3. there is no request body, since a nested command sent as a `GET` body would be invisible to (2).

Segments are matched after percent-decoding, case folding, and stripping control characters, surrounding whitespace and dots, so `/rci/system/configuration/%73ave` does not slip through.

One check is **not** waived by `--unsafe`, because it is about which machine is contacted rather than what runs there: the endpoint must be a path rooted at a single `/`. Otherwise `@evil.example/rci/show/version` would turn the router's `host:port` into URL userinfo and send the request, and any `--data-json` body, somewhere else entirely.

The gate is a pure function with tests behind it, and it errs toward blocking: some genuinely read-only requests are refused rather than risk letting a write through.

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)
- A Keenetic/Netcraze router reachable over HTTP, and an account on it with the **Web interface** permission

## Install

### Let the agent do it

Hand your agent the link to this repository and ask it to set the tool up:

> *"Set this up for me: https://github.com/dummylabs/keenetic-cli — read the README and follow it."*

It will clone the repository, create `.env` from the example, install the skill where your agent looks for skills, and replace the placeholder path inside `SKILL.md` with the real one. That is the fiddly part, and it is the part an agent is good at.

Two steps stay with you, because nobody can do them on your behalf: creating the user account on the router, and entering the password. Both are described below — tell the agent what username you created and it will fill in the rest.

### Or do it by hand

```bash
git clone https://github.com/dummylabs/keenetic-cli.git
cd keenetic-cli
cp .env.example .env
```

Fill in `KEENETIC_HOST` and `KEENETIC_USERNAME` in `.env`. The password is covered [below](#the-password) — it can go in the same file or, on macOS, in the keychain.

Then install the skill as described in [The agent skill](#the-agent-skill).

### The router account

Create a dedicated user on the router rather than reusing the admin account. In the web interface: **Management → Users → add user**.

Tick **Web interface**. That is the only permission this tool needs, and it covers everything, including writes.

Do **not** tick **Prohibit saving system settings** if you want `set policy` to work: on Keenetic/Netcraze, write access is the default state and that checkbox takes it away.

> Note: some Keenetic/Netcraze firmware rejects a hyphen in the username. `keenetic_cli` works.

### The password

There are two places the password can live, and the CLI reads them in this order:

1. `KEENETIC_PASSWORD` — from the environment or from `.env`
2. the macOS keychain

Whichever comes first wins, so setting `KEENETIC_PASSWORD` means the keychain is never consulted.

#### Password in .env file

**On any system**, put the password in `.env` next to the other settings:

```
KEENETIC_PASSWORD=your-router-password
```

This is the only option outside macOS, and it is a perfectly fine one anywhere: the file sits in your own home directory.

#### Password in macOS keychain

**On macOS** you can instead keep it in the keychain, so no file on disk holds it in the clear:

```bash
security add-generic-password -U -s keenetic -a <router-username> -w
```

Running this opens a prompt — paste the password there. `security` is the native macOS keychain tool, and typing the password into its prompt keeps it out of your shell history.

Leave `KEENETIC_PASSWORD` unset (or commented out) in `.env` for the keychain to be used.

The keychain item is keyed by the *router* username, so pointing `--env-file` at a second router looks up that router's own password instead of silently reusing this one's.

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

`--mac` and `--name` are mutually exclusive and one is required. `--policy` accepts `default`, `not_internet`, a policy id, or a policy's exact description.

A policy change is confirmed by reading the state back, because the router reports failure inside a success response. The result also says whether the change was **persisted** — if the batched `system configuration save` failed, the policy is live but will not survive a reboot, and that is reported separately rather than as a rejected write.

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

`--errors` shows `Error`/`Critical`/`Fatal` entries plus problem-shaped network messages such as `timeout`, `failed`, `did not complete`, `stopped hearing back` and `retrying handshake`.

### Free IP addresses

```bash
uv run keenetic_cli.py show dhcp
uv run keenetic_cli.py show dhcp --occupied
uv run keenetic_cli.py show dhcp --json
```

Reports the DHCP pool bounds, what is occupied (reservations, active leases, and hosts merely seen at an address), and **two** lists of free addresses.

Two lists, not one, because they are different claims. Only an address **outside the pool** is safe to configure statically on a device; one inside the pool is free this second and the router may lease it to the next machine that asks.

Occupancy is counted from two sources: `/rci/show/ip/dhcp/bindings` does not know about an address configured on the device itself, and the hotspot registry does not know about a reservation for a host that is currently offline.

### Raw API calls

Any RCI endpoint can be called directly. Reading is free; anything that changes the router the CLI refuses until you say you meant it — see [Safety model](#safety-model) for why the line falls where it does.

```bash
uv run keenetic_cli.py api request --method GET --endpoint /rci/show/interface
```

Any body-less `GET` on a non-action path is allowed by default. Per the RCI specification, GET retrieves settings and does not execute commands, so config reads outside `/rci/show/...` — for example `/rci/ip/policy` — need no flag.

`--unsafe` is required for `POST`/`DELETE`/`PUT`, and for `GET` on an action path (`save`, `reboot`, `reset`, `erase`, `upgrade`, and others):

```bash
uv run keenetic_cli.py api request \
  --method POST \
  --endpoint /rci/ \
  --data-json '[{"show":{"interface":{}}}]' \
  --unsafe
```

Output is redacted by default, here as everywhere else. `--no-redact` prints the router's response unmasked, and is the only way to see a raw secret.

## The agent skill

`skill/` contains a skill that teaches an agent to use this CLI: the safety rules, the command recipes, how to translate Keenetic/Netcraze CLI commands into `/rci/...` endpoints, and `command-index/` — every documented command with its endpoint, its arguments, and notes on the ones that bite.

For Claude Code:

```bash
cp -r skill ~/.claude/skills/keenetic-router-api
```

For Codex:

```bash
cp -r skill ~/.codex/skills/keenetic-router-api
```

If you use both, keep one copy and symlink the other at it, so you only edit the skill once:

```bash
cp -r skill ~/.agents/skills/keenetic-router-api
ln -s ~/.agents/skills/keenetic-router-api ~/.claude/skills/keenetic-router-api
ln -s ~/.agents/skills/keenetic-router-api ~/.codex/skills/keenetic-router-api
```

Either way, edit the installed `SKILL.md` and replace `/path/to/keenetic-cli` with wherever you cloned this repository.

The command index is copied along with the rest, so the agent finds it beside `SKILL.md` with no further setup.

## Tests

```bash
uv run tests/test_keenetic_cli.py
```

93 offline tests: no router, no network, no pytest. They cover the pure, safety-relevant logic — the unsafe-request gate, redaction, log parsing, DHCP arithmetic, and config resolution. Everything beyond that needs a live router, so try read-only commands first.

## License

MIT — see [LICENSE](LICENSE).

This project is not affiliated with or endorsed by Keenetic/Netcraze.
