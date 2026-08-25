# `known` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `known host` — changes settings

Registers a named host together with its MAC address.

**RCI** `/rci/known/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Arbitrary name assigned to the host. |
| `mac` | Host MAC address. |

**Catch:** the example shows the removal response naming a MAC different from the MAC supplied in the removal command; treat that response value as unreliable rather than as an echo.
