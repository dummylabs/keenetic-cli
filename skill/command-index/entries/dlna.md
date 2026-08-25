# `dlna` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `dlna` — read-only

Enters the command group for managing the DLNA service.

**RCI** `/rci/dlna`

**Catch:** NONE

### `dlna interface` — changes settings

Selects interfaces through which DLNA media traffic may be sent.

**RCI** `/rci/dlna/interface`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Accepts a full interface name or an alias. |

**Catch:** up to 16 interfaces may be configured, so this is a bounded list rather than an unlimited set.

**Blast radius:** bare `no interface` removes all DLNA interfaces.

### `dlna rescan` — read-only

Refreshes the media-content index for the DLNA service.

**RCI** `/rci/dlna/rescan`

**Arguments:**

| Argument | Notes |
|---|---|
| `full` | Requests deletion and reconstruction of the content database, which may be a lengthy operation. |

**Catch:** `full` is not just a broader scan: it destroys and rebuilds the existing content database, so it should not be used as a routine refresh.
