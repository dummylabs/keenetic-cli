# Keenetic command index

Derived from the Keenetic Hero KN-1011 CLI Command Reference Guide, OS 5.0, Edition 1.164
(2026-01-30). The manuals are nearly identical across models, so the command tree and the
CLI-to-RCI mapping carry over; hardware-specific commands may not.

An original compilation of facts about the API surface — command names, `/rci` paths, argument
names and types, the manual's yes/no metadata — with written notes. It does not reproduce the
vendor's prose.

## How to use it

1. `grep` **`commands.csv`** for the command, or for a word in it.
2. The `rci` column is the endpoint. It is always `'/rci/' + cmd.replace(' ', '/')`.
3. The `entry` column names the file holding the written note, where one exists.

## The two levels

**`commands.csv`** — 904 commands, one row each, 14 columns: `ref`, `cmd`, `family`, `rci`,
`changes_settings`, `no_prefix`, `no_wipes_list`, `multiple_input`, `context`, `interface_type`,
`args`, `required_args`, `source`, `entry`.

**`entries/*.md`** — 742 written entries in 66 files. Each carries a one-line summary,
the RCI path, argument notes, and a **Catch** naming the trap a caller falls into.
`**Catch:** NONE` means the block held no trap; it is an honest answer, not a gap.

Two lines appear only where the manual justifies them:

- **Blast radius** (43 commands) — the bare `no` form, called without its selector, removes the
  whole list rather than one item, and the line says what is lost.
- **Destructive** (5 commands) — the effect cannot simply be undone: `erase`,
  `system configuration factory-reset`, `system configuration save`, `opkg disk`, `system button`.
  Saving counts, because it makes the current running state permanent, including changes the
  caller did not mean to keep.

Covered: every read-only command, every list-clearing command, the whole `interface` and `ip`
families, and the everyday `system`, `service`, `dns-proxy`, `ipv6`, `user`, `schedule`,
`components`, `dyndns` and `ping-check` surface. The remaining 162 — mostly `crypto`
(IPsec), the VPN-server tuning knobs, and appliance features such as `printer`, `dlna`, `snmp`
and `torrent` — are in `commands.csv` only.

## Known corrections to the generated data

- `system zram` was marked `no_wipes_list = yes`. The manual says omitting the argument sets the
  zRam size **automatically**; it clears no list. Corrected to `no`.
- `interface tx-queue scheduler fq_codel` (§3.29.224) was **missing**. Its heading fell inside a
  fenced code block during PDF conversion, so every heading-based parser skipped it — including
  the coverage check, which counted headings the same way. Added.
- `tools ping6`: the manual's synopsis names the option `packetsize` while its own example writes
  `size`. The source contradicts itself; neither spelling has been tested.

## Caveats

Nothing here has been run against a live router. RCI JSON field names are **not** always the CLI
argument names shown here — CLI `sni <fqdn>` is JSON `fqdn`, and a wrong field name is accepted
silently while the command reports success. Read an existing object back before writing a new one,
and re-read afterwards.

## Largest entry files

| File | Entries | Size |
|---|---:|---:|
| `interface-other` | 153 | 51 KB |
| `show-other` | 78 | 37 KB |
| `ip-other` | 39 | 17 KB |
| `system` | 35 | 13 KB |
| `ip-http` | 34 | 11 KB |
| `dns-proxy` | 22 | 11 KB |
| `show-interface` | 21 | 11 KB |
| `ip-dhcp` | 26 | 9 KB |
| `interface-ip` | 26 | 9 KB |
| `mws` | 22 | 8 KB |
