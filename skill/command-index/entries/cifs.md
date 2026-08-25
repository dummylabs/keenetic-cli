# `cifs` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `cifs` — read-only

Enters the configuration context for managing the CIFS service.

**RCI** `/rci/cifs`

**Catch:** NONE

### `cifs automount` — changes settings

Controls automatic mounting of USB storage for CIFS access.

**RCI** `/rci/cifs/automount`

**Catch:** NONE

### `cifs map-hidden` — changes settings

Controls CIFS support for ACLs and hidden files.

**RCI** `/rci/cifs/map-hidden`

**Catch:** the example prints `Map hidden enabled` after both enabling and disabling, although the block says the `no` form disables the feature; the response text therefore does not reliably indicate the resulting state.

### `cifs permissive` — changes settings

Controls whether CIFS file access is open to all users or restricted.

**RCI** `/rci/cifs/permissive`

**Catch:** disabling permissive mode restricts file access to users carrying the `cifs` tag.

### `cifs share` — changes settings

Creates a CIFS share rooted at a USB-storage path.

**RCI** `/rci/cifs/share`

**Arguments:**

| Argument | Notes |
|---|---|
| `label` | The share name exposed to users. |
| `mount` | May identify either the storage root or a subdirectory. |
| `description` | Optional text describing the share. |

**Catch:** the obsolete `timemachine` setting is not available in this command's arguments, although the block says it is enabled by default for all shares.

**Blast radius:** bare `no share` removes every CIFS share.
