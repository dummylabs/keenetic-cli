---
name: keenetic-router-api
description: "Use when the agent needs to inspect or manage a Keenetic/Netcraze router through the local Python CLI and the Keenetic/Netcraze Web API (RCI). Triggers include: Keenetic API, Netcraze API, router interfaces, WireGuard/OpenVPN/ZeroTier state, show interfaces, show interface-stat, show log, show dhcp, running Keenetic/Netcraze CLI commands, translating Keenetic/Netcraze CLI commands to /rci endpoints, or safely calling raw router API requests."
---

# Keenetic/Netcraze Router API

Use the local CLI wrapper instead of raw `curl`/HTTP. It handles Keenetic/Netcraze authentication and has a safety guard for read-only API calls.

## Project paths

Replace `/path/to/keenetic-cli` below with wherever you cloned this repository, then keep the rest of this file as-is.

- Project root: `/path/to/keenetic-cli`
- CLI tool: `/path/to/keenetic-cli/keenetic_cli.py`
- CLI config: `/path/to/keenetic-cli/.env`
- CLI README: `/path/to/keenetic-cli/README.md`

Run commands from the project root:

```bash
cd /path/to/keenetic-cli
uv run keenetic_cli.py ...
```

## Safety rules

- Start with read-only diagnostics.
- Prefer high-level `show ...` CLI commands when they exist.
- For raw API, **any `GET` is allowed by default** — the RCI spec defines GET as retrieving settings and "not applicable" to actions other than `/rci/show`, so it does not execute commands. Config reads such as `GET /rci/dns-proxy/filter/profile` need no flag; use them freely to inspect state.
- `--unsafe` is required for anything that can change the router: `POST`/`DELETE`/`PUT`, plus `GET` on an action path (`save`, `reboot`, `reset`, `erase`, `upgrade`, …), which stays gated in case "not applicable" is not a no-op. So the flag now means what it says — treat every `--unsafe` call as a change that needs user approval and post-verification.
- Do not use `--no-redact` unless the user explicitly needs full secrets/keys; JSON output is redacted by default.
- Do not save router configuration unless explicitly asked. Saving is an unsafe operation.

### Verify against running config, never saved config

After any mutating request, verify against the **running** config:

- `{"show":{"rc":{...}}}` (nested batch form) is the live state.
- `{"show":{"sc":{...}}}` is the last **saved** state and will differ until `system configuration save`.
- The GET path form `/rci/show/sc/...` is **not** equivalent to the nested batch and must not be used to tell the two apart — it has been observed returning running-config content.
- The Keenetic/Netcraze **web UI renders `sc`**, so it shows stale state until a save. Never verify by screenshot, and warn the user that saving anything from a stale UI page may write the old configuration back over the running one.

A bare `show ...` without `rc`/`sc` is ambiguous. Say which one you checked when reporting success.

### Removals can clear an entire list

Many `no ...` / delete operations wipe the **whole list** when the selector is omitted, and some ignore a JSON body selector entirely (`DELETE /rci/ip/host` takes its selector in the query string; passing it in the body silently deleted every user static host record).

Before any removal:

1. Read the current list first.
2. Establish how many entries would be lost **if the selector were ignored** — that is the blast radius.
3. Proceed only once that radius is known and acceptable; say it out loud before acting.

Prefer removals scoped to a named object (`filter profile <name> tls upstream ...`) over global ones.

### RCI JSON field names differ from CLI keywords

The CLI syntax `sni <fqdn>` maps to the JSON field **`fqdn`**, not `sni`. A wrong field name is **silently ignored and the command still reports success** — producing a half-configured object.

- Before writing a new object type, `GET` the config path of an existing working one (e.g. `GET /rci/dns-proxy/filter/profile`) and copy its exact field names.
- After writing, re-read and confirm every field you intended to set is actually populated.
- Note that list-valued settings often **append** rather than replace (`tls upstream` allows up to 6 servers), so overwriting means removing the old entry first.

## Common CLI tasks

Inspect interfaces:

```bash
uv run keenetic_cli.py show interfaces
uv run keenetic_cli.py show interfaces --connected
uv run keenetic_cli.py show interfaces --type wireguard
uv run keenetic_cli.py show interfaces --name Wireguard0 --json
```

Inspect interface statistics:

```bash
uv run keenetic_cli.py show interface-stat --name Wireguard0
```

Inspect router logs:

### Free IP addresses and DHCP occupancy

```bash
uv run keenetic_cli.py show dhcp
uv run keenetic_cli.py show dhcp --occupied
uv run keenetic_cli.py show dhcp --json
```

Use this instead of asking the user which address to take. It reports the pool bounds, what is occupied (reservations, active leases, and hosts merely seen at an address), and two lists of free addresses.

**Only `free_outside_pool` may be assigned statically on a device.** An address in `free_inside_pool` is free right now but sits inside the DHCP range, so the router may lease it to the next machine that asks. Recommending one of those is how address collisions happen.

```bash
uv run keenetic_cli.py show log
uv run keenetic_cli.py show log --since-minutes 30 --errors
uv run keenetic_cli.py show log --lines 500 --grep wireguard
```

Use `show log --errors` to focus on Error/Critical/Fatal entries and problem-like network messages such as timeouts, failed handshakes, and unreachable peers.

List known clients and policies:

```bash
uv run keenetic_cli.py list clients
uv run keenetic_cli.py list clients --include-inactive
uv run keenetic_cli.py list policies
```

Set a client policy (mutating; only do this when requested):

```bash
uv run keenetic_cli.py set policy --name exact-hostname --policy default
uv run keenetic_cli.py set policy --mac aa:bb:cc:dd:ee:ff --policy home_policy
```

## Raw API calls through the CLI

Use `api request` for endpoints not covered by high-level commands.

Safe read-only example:

```bash
uv run keenetic_cli.py api request --method GET --endpoint /rci/show/interface
```

Unsafe example, only after explicit approval/intent:

```bash
uv run keenetic_cli.py api request \
  --method POST \
  --endpoint /rci/ \
  --data-json '[{"show":{"interface":{}}}]' \
  --unsafe
```

Options to remember:

- `--method GET|POST|DELETE|...` default is `GET`.
- `--endpoint /rci/...` is required.
- `--data-json '...'` accepts inline JSON only.
- `--raw` prints compact JSON.
- `--no-redact` disables secret masking; avoid it by default.
- `--unsafe` is required for `POST`/`DELETE`/`PUT`, and for `GET` on an action path (`save`, `reboot`, `reset`, `erase`, `upgrade`, …). Any other `GET` needs no flag.

If a raw call is blocked, explain that default mode permits any body-less `GET` on a non-action path, and that this endpoint was blocked because it names an action; ask for/confirm unsafe intent before retrying with `--unsafe`.

## Translating Keenetic/Netcraze CLI commands to RCI endpoints

Use the docs before inventing endpoints. The rule of thumb:

```text
CLI:  show interface
REST: /rci/show/interface

CLI:  show interface name=Wireguard0
REST: /rci/show/interface/Wireguard0
REST: /rci/show/interface?name=Wireguard0

CLI:  show interface stat name=Wireguard0
REST: /rci/show/interface/stat?name=Wireguard0

CLI:  system configuration save
REST: /rci/system/configuration/save  (unsafe)
```

Parameter placement rules:

- CLI command words and subcommands become path segments: `show interface stat` -> `/rci/show/interface/stat`.
- Named resources on `show` commands, especially `name=<id>`, are often accepted either as a path segment or as a query parameter: `/rci/show/interface/Wireguard0` and `/rci/show/interface?name=Wireguard0`.
- Subcommands such as `stat`, `mac`, `rrd`, or other command nouns stay in the path; their narrowing argument stays a query parameter: `/rci/show/interface/stat?name=Wireguard0`.
- If unsure, prefer the documented subcommand path plus query parameters, because it preserves the CLI command structure and keeps identifiers out of the command path.

Arguments from the manual can be passed as query parameters or JSON body. Batch/nested requests use `POST /rci/` with JSON and require `--unsafe` in this CLI even when the nested command is read-only.

## Keenetic/Netcraze command reference

This repository does not bundle Keenetic/Netcraze's command reference: it is the vendor's copyrighted manual, not ours to redistribute. Get the CLI manual for your model from Keenetic/Netcraze's own documentation site and keep it where you can read it, for example
<https://storage.googleapis.com/docs.help.keenetic.com/cli/5.0/en/cli_manual_kn-1011.pdf>
(that one is for the KN-1011, but the manuals are nearly identical across models).

If you convert that manual to Markdown, put it somewhere local and add the paths here so the agent can grep it instead of guessing endpoints. The mapping in the previous section is enough for the common cases; the manual matters when you need an endpoint this CLI has no command for.

## Workflow

1. Identify whether the task is read-only inspection or mutation.
2. For common interface/client/policy tasks, use high-level CLI commands.
3. For unknown commands, consult the Keenetic/Netcraze CLI manual for the router model in question.
4. Convert CLI command path to `/rci/...` endpoint and choose method/body from the docs.
5. Run any read-only `GET` directly, including config reads outside `/rci/show/...`; ask/confirm before `--unsafe` when mutation or a batched `POST /rci/` is involved.
6. Summarize results with redacted secrets and include the exact command used when useful.
