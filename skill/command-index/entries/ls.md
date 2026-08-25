# `ls` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ls` — read-only

Lists entries in a filesystem directory.

**RCI** `/rci/ls`

**Arguments:**

| Argument | Notes |
|---|---|
| `directory` | Filesystem-qualified path in the form `<file system>:<path>`, such as `flash`, `temp`, `proc`, or `usb`. |

**Catch:** Entries repeat under the `entry` key, and the example shows directory records with `type: D` lacking `size` while the file record has `type: R` and a size; do not assume every entry has the same fields.

**Returns (fields):** `rel`, `entry`, `type`, `name`, `size`.
