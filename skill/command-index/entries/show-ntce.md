# `show` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `show ntce applications` — read-only

Lists applications supported by the NTCE service and their classification metadata.

**RCI** `/rci/show/ntce/applications`

**Catch:** the example includes an application whose `group-long` is `Removed` while it still has a `groupset-short-id` and `groupset-long-id`; consumers should not discard a record merely because its group is marked removed.

**Returns (fields):** `application`, `id-num`, `short`, `long`, `group-id`, `group-long`, `groupset-id`, `groupset-short-id`, `groupset-long-id`.

### `show ntce attributes` — read-only

Enumerates NTCE connection attributes and their numeric identifiers.

**RCI** `/rci/show/ntce/attributes`

**Catch:** records repeat under `attribute`, so the numeric `id-num` must be retained as a record value rather than treating the output as one attribute map.

**Returns (fields):** `attribute`, `id-num`, `short`, `long`.

### `show ntce filter profile` — read-only

Lists NTCE filter profiles or inspects one named profile.

**RCI** `/rci/show/ntce/filter/profile`

**Catch:** NONE

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | String | Selects an NTCE filter profile. |

**Returns (fields):** `profile`, `name`, `type`, `schedule`, `schedule-active`.

### `show ntce groups` — read-only

Provides the NTCE service's group catalogue and its group-set classification.

**RCI** `/rci/show/ntce/groups`

**Catch:** each result is a repeated `group` record, while the group-set identifiers and labels recur across many groups; do not treat any of those classification fields as a unique group key.

**Returns (fields):** `group`, `id-num`, `long`, `groupset-id`, `groupset-short-id`, `groupset-long-id`.

### `show ntce groupsets` — read-only

Provides the NTCE service's group-set catalogue.

**RCI** `/rci/show/ntce/groupsets`

**Catch:** results arrive as repeated `groupset` records, so a parser that stores one value per key would retain only the final group-set.

**Returns (fields):** `groupset`, `id-num`, `short`, `long`.

### `show ntce hosts` — read-only

Reports NTCE-detected application traffic together with host details.

**RCI** `/rci/show/ntce/hosts`

**Catch:** the example places many repeated `application` records inside a `host` section and then emits host metadata in another `host` section for the same MAC; parse the repeated records and their nesting rather than assuming one flat host object. The example also shows an application record where `group-long` is present but the surrounding layout is irregular, so do not rely on column alignment.

**Returns (fields):** `host`, `mac`, `application`, `id-num`, `short`, `long`, `group-id`, `group-long`, `groupset-id`, `groupset-short-id`, `groupset-long-id`, `groupset-service-class`, `rxbytes`, `txbytes`, `os-id`, `os-long`, `via`, `ip`, `hostname`, `name`, `interface`, `id`, `description`, `dhcp`, `static`, `registered`, `access`, `schedule`, `active`, `uptime`, `first-seen`, `last-seen`, `link`, `auto-negotiation`, `speed`, `duplex`, `port`, `traffic-shape`, `rx`, `tx`, `mode`.

### `show ntce oses` — read-only

Provides the NTCE service's operating-system catalogue.

**RCI** `/rci/show/ntce/oses`

**Catch:** operating systems are emitted as repeated `os` records, not as a single map keyed by `id-num`.

**Returns (fields):** `os`, `id-num`, `long`.

### `show ntce status` — read-only

Reports NTCE connection-tracking, event, database, and memory counters.

**RCI** `/rci/show/ntce/status`

**Catch:** `memory` occurs in both the event and database sections, and `total` occurs in their respective memory records; flattening by field name alone will conflate separate counters.

**Returns (fields):** `conntrack`, `hosts`, `applications`, `applications-flows`, `applications-events`, `groups`, `groups-flows`, `groups-events`, `memory`, `total`, `event`, `count`, `database`, `attributes`.
