# `schedule` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `schedule` — changes settings

Creates or selects a schedule configuration context by name.

**RCI** `/rci/schedule`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Schedule name. |

**Catch:** Selecting a name that is not yet present creates the schedule instead of failing; the `no` form deletes the selected schedule.

### `schedule action` — changes settings

Associates a start or stop action with a scheduled time.

**RCI** `/rci/schedule/action`

**Arguments:**

| Argument | Notes |
|---|---|
| `action` | `start` marks the beginning action; `stop` marks the ending action. |
| `min` | Minute value for the scheduled action. |
| `hour` | Hour value for the scheduled action. |
| `dow` | Comma-separated days of the week; `0` is Sunday and `*` means every day. |

**Catch:** NONE

### `schedule description` — read-only

Sets the description of the selected schedule.

**RCI** `/rci/schedule/description`

**Arguments:**

| Argument | Notes |
|---|---|
| `description` | The schedule's description text. |

**Catch:** using the no-prefix form deletes the selected schedule's description altogether.

---

### `schedule led` — changes settings

Chooses whether the selected schedule's start or stop event drives its LED indication.

**RCI** `/rci/schedule/led`

**Arguments:**

| Argument | Notes |
|---|---|
| `action` | `start` indicates the beginning event; `stop` indicates the ending event. |

**Catch:** LED control is effective only after the schedule is selected by the separate `system led` configuration.
