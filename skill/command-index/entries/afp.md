# `afp` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `afp` — read-only

Enters the configuration context for managing the AFP server service.

**RCI** `/rci/afp`

**Catch:** NONE

### `afp automount` — changes settings

Controls automatic mounting of USB storage for AFP access.

**RCI** `/rci/afp/automount`

**Catch:** NONE

### `afp permissive` — changes settings

Controls whether AFP file access is open to all users or restricted.

**RCI** `/rci/afp/permissive`

**Catch:** disabling permissive mode restricts file access to users carrying the `afp` tag.

### `afp share` — changes settings

Creates an AFP share rooted at a USB-storage path.

**RCI** `/rci/afp/share`

**Arguments:**

| Argument | Notes |
|---|---|
| `label` | The share name exposed to users; the example submits `AFP_TEST2` twice and receives an add confirmation both times, so do not assume repeating a label is an update. |
| `mount` | May identify either the storage root or a subdirectory. |
| `description` | Optional text describing the share. |

**Catch:** the obsolete `timemachine` setting is not an argument in the current syntax, while the block says the attribute defaults to enabled for every share.

**Blast radius:** bare `no share` removes every AFP share, not just an unspecified one.
