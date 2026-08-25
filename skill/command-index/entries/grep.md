# `grep` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `grep` — read-only

Filters show-command output using a regular-expression match.

**RCI** `/rci/grep`

**Arguments:**

| Argument | Notes |
|---|---|
| `command` | The show command whose XML response is searched. |
| `a` | Number of output lines retained after a match. |
| `b` | Number of output lines retained before a match. |
| `c` | XML-context nesting depth around a match, rather than a line count. |
| `pattern` | The expression is matched against XML node names and values. |

**Catch:** `-C` uses XML nesting depth, while `-A` and `-B` use line counts, so the three context switches do not measure the same kind of surrounding output.

**Returns (fields):** `ndw`, `features`, `version`, `components`, `release`, `sandbox`, `title`, `arch`, `ndm`, `exact`, `cdate`, `bsp`, `ndw3`, `ndw4`, `manufacturer`, `vendor`, `series`, `model`, `hw_version`, `hw_type`, `hw_id`, `device`, `consent`, `region`, `description`.
