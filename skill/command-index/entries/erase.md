# `erase` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `erase` — changes settings

Deletes a named file from the Hero device.

**RCI** `/rci/erase`

**Arguments:**

| Argument | Notes |
|---|---|
| `filename` | File to remove. |

**Catch:** NONE

**Destructive:** the specified file is erased; the block does not state whether the deletion can be recovered or what other data, if any, survives.
