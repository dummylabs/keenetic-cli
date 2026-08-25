# `ppe` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ppe` — changes settings

Selects the software or hardware Packet Processing Engine accelerator.

**RCI** `/rci/ppe`

**Arguments:**

| Argument | Notes |
|---|---|
| `engine` | `software` selects the software accelerator; `hardware` selects the hardware accelerator. |

**Catch:** The example's bare `no ppe` disables all PPE, not merely one selected engine.
