# `ntp` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ntp` — read-only

Accesses the NTP client configuration.

**RCI** `/rci/ntp`

**Catch:** the no-prefix form resets the entire NTP client configuration to its default, rather than changing one individual setting.

---

### `ntp master` — changes settings

Enables the router's SNTP server for private and protected network segments.

**RCI** `/rci/ntp/master`

**Catch:** the `no` form stops the SNTP service rather than restoring a parameter value.

### `ntp server` — changes settings

Adds an NTP server to the router's server list.

**RCI** `/rci/ntp/server`

**Arguments:**

| Argument | Notes |
|---|---|
| `server` | NTP server hostname or other server string. |

**Catch:** calls add servers to the list rather than replacing the current value, but the list is capped at eight servers.

**Blast radius:** bare `no ntp server` removes all configured NTP servers.

### `ntp source` — changes settings

Sets the source IP address used by the NTP service.

**RCI** `/rci/ntp/source`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Source IP address for all NTP packets. |

**Catch:** NONE

### `ntp sync-period` — changes settings

Sets the interval between time-synchronization operations.

**RCI** `/rci/ntp/sync-period`

**Arguments:**

| Argument | Notes |
|---|---|
| `period` | Interval in minutes, from 60 minutes through one month; the documented default is one week. |

**Catch:** NONE
