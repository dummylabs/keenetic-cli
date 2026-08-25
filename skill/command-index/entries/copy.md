# `copy` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `copy` — read-only

Copies file contents between source and destination paths.

**RCI** `/rci/copy`

**Arguments:**

| Argument | Notes |
|---|---|
| `source` | Full source path in `<file system>:<path>` form. |
| `destination` | Full destination path in `<file system>:<path>` form. |

**Catch:** the examples use aliases rather than literal filesystem paths: `running-config` means `system:running-config`, `startup-config` means `flash:startup-config`, and `MyPassport:/log.txt` supplies an explicit filesystem.
