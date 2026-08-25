# `tools` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `tools` — read-only

Enters the command group for testing the environment.

**RCI** `/rci/tools`

**Catch:** NONE

### `tools arping` — read-only

Probes an IPv4 respondent at the link layer and emits replies as the operation progresses.

**RCI** `/rci/tools/arping`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | The IPv4 respondent to probe. |
| `source-interface` | Selects the interface from which the ARP probes originate. |
| `count` | Sets a finite probe count; without it, the operation remains active until the user interrupts it. |
| `wait-time` | Sets the maximum wait for a response in milliseconds. |

**Catch:** omitting `count` makes this a long-running interactive operation rather than a bounded request; replies are printed as they arrive and the completion summary appears only when the process ends.

**Returns (report labels):** `Starting the ARP ping`, `ARPING`, `Unicast reply from`, `Sent`, `received`, `Process terminated`.

### `tools ping` — read-only

Measures ICMP reachability and round-trip timing for a named or addressed host.

**RCI** `/rci/tools/ping`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Accepts either a domain name or a host IP address. |
| `count` | Sets the number of requests; without it, probing continues until the user interrupts it. |
| `packetsize` | Defaults to 56 bytes and accepts 28–65535 bytes. |
| `sequence-id` | Defaults to 0 and accepts 0–65535. |
| `source` | Can select either a source address or a source interface. |
| `tos` | Defaults to 0 and accepts 0–63. |
| `ttl` | Defaults to 30 and accepts 1–255. |

**Catch:** the documented size argument is `packetsize`, but the examples invoke `size`; treat that spelling mismatch as an inconsistency in the block rather than relying on the example as the argument name. With no `count`, the command is an ongoing stream of probe output until interrupted.

**Returns (report labels):** `Sending ICMP ECHO request`, `PING`, `bytes from`, `packets transmitted`, `packet loss`, `duplicate(s)`, `Round-trip`, `Process terminated`.

### `tools ping6` — read-only

Measures ICMPv6 reachability and round-trip timing for an IPv6 host.

**RCI** `/rci/tools/ping6`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Accepts a domain name or an IPv6 host address. |
| `count` | Sets the number of requests; without it, probing continues until the user interrupts it. |
| `packetsize` | Defaults to 56 bytes and accepts 28–65535 bytes. |
| `sequence-id` | Defaults to 0 and accepts 0–65535. |
| `source` | Can select either a source address or a source interface. |
| `tos` | Defaults to 0 and accepts 0–63. |
| `ttl` | Defaults to 30 and accepts 1–255. |

**Catch:** the synopsis and argument table name the size option `packetsize`, but the worked example writes `size 111`. The two disagree, so do not copy the spelling out of the example without checking which one the firmware accepts.

**Returns (report labels):** `sending ICMPv6 ECHO request`, `PING`, `bytes from`, `packets transmitted`, `packet loss`, `duplicate(s)`, `Round-trip`.

### `tools traceroute` — read-only

Collects the sequence of responding hops toward a target using a selectable probe protocol.

**RCI** `/rci/tools/traceroute`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Names the target host. |
| `count` | Defaults to 3 probes per hop and accepts 1–10. |
| `interval` | Defaults to 0 seconds between probes and accepts 0–15 seconds. |
| `wait-time` | Defaults to 1 second per probe response and accepts 1–15 seconds. |
| `packetsize` | For `tcp`, only 52 is allowed; for `udp` and `icmp`, the default is 60 and the allowed range is 28–65535. |
| `max-ttl` | Defaults to 30 hops and accepts 1–255. |
| `port` | Defaults by protocol: 80 for `tcp`, 33434 for `udp`, and 1 for `icmp`. |
| `source-address` | Selects the source address for outgoing probes. |
| `source-interface` | Selects the source interface for outgoing probes. |
| `type` | Selects `tcp`, `udp`, or `icmp`; `udp` is the default. |
| `tos` | Defaults to 0 and accepts 0–255. |

**Catch:** changing `type` changes the implicit `packetsize` and `port` defaults as well, so a protocol switch can alter the probes even when those two arguments are omitted. The example prints hop results in a human-readable trace and then a termination line, not a keyed result set.

**Returns (report labels):** `starting traceroute`, `traceroute to`, hop entries, `process terminated`.
