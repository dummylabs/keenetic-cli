# `ussd` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ussd send` — read-only

Submits a USSD request through a selected mobile interface and presents the operator's reply.

**RCI** `/rci/ussd/send`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Accepts a full interface name or an alias. |
| `request` | Carries the USSD command sent to the mobile operator. |

**Catch:** NONE

**Returns (fields):** `request`, `response`.
