# `pppoe` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `pppoe pass` — changes settings

Configures PPPoE pass-through between a WAN interface and a LAN interface.

**RCI** `/rci/pppoe/pass`

**Arguments:**

| Argument | Notes |
|---|---|
| `wan-iface` | Starting WAN interface, supplied by full name or alias. |
| `lan-iface` | Finishing LAN interface, supplied by full name or alias. |

**Catch:** The example resolves the supplied aliases to full interface names in its confirmation, so callers should not assume that the response repeats the argument strings.
