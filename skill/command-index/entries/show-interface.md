# `show` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `show interface` — read-only

Reports the state of the selected interface and any subordinate interface information included for that interface.

**RCI** `/rci/show/interface`

**Catch:** the response shape depends on the interface type: the example for `GigabitEthernet0` includes physical-port records, and one port additionally carries a `role` record, so callers must not assume that every interface has the same fields or children.

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Accepts either the interface's full name or an alias. |

**Returns (fields):** `id`, `index`, `type`, `description`, `interface-name`, `link`, `connected`, `state`, `mtu`, `tx-queue`, `port`, `speed`, `duplex`, `auto-negotiation`, `flow-control`, `eee`, `last-change`, `last-overflow`, `public`, `role`.

### `show interface antennas` — read-only

Reports per-antenna signal measurements for a USB mobile interface.

**RCI** `/rci/show/interface/antennas`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** the measurements are technology-dependent: `rsrq`, `rsrp`, and `phase` apply only to 4G, while `ecio` applies only to 3G, so the field set is not stable across connections.

**Returns (fields):** `antenna`, `channel`, `rssi`, `rsrq`, `rsrp`, `phase`, `ecio`.

### `show interface bands` — read-only

Lists the 3G and LTE radio bands a mobile interface offers, each with its own enabled flag.

**RCI** `/rci/show/interface/bands`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** bands are listed under two different parent keys, `umts` and `lte`, and each band carries its own `enabled` flag — the command reports every available band, not only the active ones, so filtering on `enabled` is the caller's job.

**Returns (fields):** `umts`, `band`, `enabled`, `lte`.

### `show interface bridge` — read-only

Reports the members and link state of a bridge interface.

**RCI** `/rci/show/interface/bridge`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** bridge members are repeated records under `members`; in the example, one member carries `inherited: yes` while the other omits `inherited`, so that attribute is not guaranteed on every member.

**Returns (fields):** `members`, `interface`, `link`, `inherited`.

### `show interface cells` — read-only

Lists the mobile-network base stations visible to a USB interface.

**RCI** `/rci/show/interface/cells`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** the response is a repeated `cells` record, not a single cell object; collect all records.

**Returns (fields):** `cells`, `phy-id`, `rssi`.

### `show interface channel-utilization rrd` — read-only

Reads time-series samples from the Wi-Fi channel-utilization monitor.

**RCI** `/rci/show/interface/channel-utilization/rrd`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full name or alias of the Wi-Fi interface. |
| `attribute` | — | The documented choices are `load` and `valid`. |
| `detail` | — | Levels 0–3 select different sample resolutions; level 0 is the default. |

**Catch:** samples are repeated `data` records, each carrying a timestamp `t` and value `v`; the example is one capture and should not be treated as a fixed number of samples or a fixed value range.

**Returns (fields):** `data`, `t`, `v`.

### `show interface channels` — read-only

Lists the channel capabilities reported by a radio interface.

**RCI** `/rci/show/interface/channels`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** the output key is inconsistent with the documented schema: the output description names `vhc-80`, but the example emits `vht-80`. Also, channel records are repeated under `channel` and carry an explicit `index`, so preserve that index rather than using the channel number as the record key.

**Returns (fields):** `channels`, `channel`, `index`, `number`, `ext-40-above`, `ext-40-below`, `vhc-80`, `vht-80`.

### `show interface chilli` — read-only

Reports RADIUS-hotspot client session statistics for an interface.

**RCI** `/rci/show/interface/chilli`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** the example uses zero for `end-time` and for every limit and speed field; the block does not define whether those zeros are sentinels for “not ended” or “unlimited,” so do not interpret them without verification.

**Returns (fields):** `host`, `session-id`, `user`, `ip`, `mac`, `start-time`, `end-time`, `idle-time`, `idle-time-limit`, `tx-bytes`, `tx-bytes-limit`, `rx-bytes`, `rx-bytes-limit`, `tx-speed`, `tx-speed-limit`, `rx-speed`, `rx-speed-limit`.

### `show interface country-codes` — read-only

Lists the country codes available on a radio interface.

**RCI** `/rci/show/interface/country-codes`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** the documented hierarchy calls the root `country-codes` and the records `code`, but the example wraps each record as `country-code`; do not assume the displayed record key matches the output description.

**Returns (fields):** `country-codes`, `country-code`, `code`, `country`.

### `show interface mac` — read-only

Prints the switch's MAC-address table.

**RCI** `/rci/show/interface/mac`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** NONE

**Returns (text table columns):** `Port`, `MAC`, `Aging`.

### `show interface name-server` — read-only

Lists DNS resolvers currently associated with an interface.

**RCI** `/rci/show/interface/name-server`

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | Full interface name or alias. |

**Catch:** resolver records have different shapes: ordinary `server` entries include `service`, while the example's `server-tls` entry instead includes `sni` and `spki` and omits `service`; parse by record type rather than requiring one common field set. The example also shows blank `interface` and `domain` values for the manager-provided servers, so blank values are possible.

**Returns (fields):** `server`, `server-tls`, `address`, `port`, `domain`, `global`, `service`, `interface`, `sni`, `spki`.

### `show interface operators` — read-only

Lists mobile operators found by the modem scan.

**RCI** `/rci/show/interface/operators`

**Catch:** this is not an on-demand scan: the interface scan must have completed first, and the resulting list remains available until the modem restarts. The example also shows the same PLMN under separate 3G and 4G records, so PLMN alone is not a unique operator record.

**Returns (fields):** `scanning`, `age`, `operator`, `plmn`, `name`, `mobile`, `status`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface rf e2p` — read-only

Reads the calibration data cells from a radio interface.

**RCI** `/rci/show/interface/rf/e2p`

**Catch:** the output is not fields at all but a hex dump of calibration cells printed as `[offset]:value` pairs across several columns; there are no key names to address, only offsets.


**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface rrd` — read-only

Provides historical receive or transmit rate samples for an interface.

**RCI** `/rci/show/interface/rrd`

**Catch:** `detail` changes the sample interval, not merely the amount of history; the examples show one-second spacing by default and two-second spacing with detail `1`, while transmit samples in the default capture are three seconds apart. Do not infer one fixed cadence from the command name.

**Returns (fields):** `data`, `t`, `v`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |
| `attribute` | `rxspeed` or `txspeed` | — |
| `detail` | Integer | The documented values select different sampling intervals. |

### `show interface spectrum rrd` — read-only

Provides historical spectrum-analyzer samples for a Wi-Fi channel and attribute.

**RCI** `/rci/show/interface/spectrum/rrd`

**Catch:** omitting `detail` selects the 64-sample, one-minute resolution; it is not an unspecified default. The available choices change the resolution to three-minute or thirty-minute samples.

**Returns (fields):** `data`, `t`, `v`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |
| `channel` | Integer | — |
| `attribute` | `load`, `dfs`, `radar`, `valid`, or `active` | — |
| `detail` | Integer | Omission uses the documented one-minute resolution. |

### `show interface stat` — read-only

Reports packet, byte, error, and drop counters for an interface.

**RCI** `/rci/show/interface/stat`

**Catch:** NONE

**Returns (fields):** `rxpackets`, `rxbytes`, `rxerrors`, `rxdropped`, `txpackets`, `txbytes`, `txerrors`, `txdropped`, `timestamp`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface traffic-counter` — read-only

Reports the state and consumption of a USB interface traffic counter.

**RCI** `/rci/show/interface/traffic-counter`

**Catch:** NONE

**Returns (fields):** `enabled`, `value`, `threshold`, `limit`, `remaining`, `unit`, `trigger`, `saved`, `limit`, `threshold`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface wps pin` — read-only

Provides the access point’s WPS PIN.

**RCI** `/rci/show/interface/wps/pin`

**Catch:** the response contains an authentication credential in clear form; treat the returned PIN as secret material rather than ordinary status data.

**Returns (fields):** `pin`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface wps status` — read-only

Reports the current WPS session state for an access point.

**RCI** `/rci/show/interface/wps/status`

**Catch:** although `left` is documented as seconds, the example uses the sentinel text `infinite`; clients must accept a non-numeric value there.

**Returns (fields):** `wps`, `configured`, `auto-self-pin`, `status`, `direction`, `mode`, `left`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |

### `show interface zerotier peers` — read-only

Lists the ZeroTier peers known through an interface.

**RCI** `/rci/show/interface/zerotier/peers`

**Catch:** a peer can contain repeated identical `path` records, so paths are a list rather than a single peer attribute. The example also shows `version: -1.-1.-1` for PLANET peers; that looks like a sentinel, but the block does not define its meaning.

**Returns (fields):** `peer`, `address`, `latency`, `role`, `version`, `path`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | Interface | — |
