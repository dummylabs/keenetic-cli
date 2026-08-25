# `igmp-proxy` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `igmp-proxy` — read-only

Enters the command group for configuring IGMP.

**RCI** `/rci/igmp-proxy`

**Catch:** NONE

### `igmp-proxy fast-leave` — changes settings

Drops a port from a multicast group's forwarding entry the moment that port sends a leave message.

**RCI** `/rci/igmp-proxy/fast-leave`

**Catch:** NONE

### `igmp-proxy force` — changes settings

Forces the IGMP proxy to use one of the older protocol versions instead of automatic selection.

**RCI** `/rci/igmp-proxy/force`

**Arguments:**

| Argument | Notes |
|---|---|
| `protocol` | `igmp-v1` applies filtering to incoming packets; `igmp-v2` applies filtering to outgoing packets. |

**Catch:** the two protocol choices are directional in the block—`igmp-v1` is associated with incoming filtering and `igmp-v2` with outgoing filtering—rather than being interchangeable version labels.
