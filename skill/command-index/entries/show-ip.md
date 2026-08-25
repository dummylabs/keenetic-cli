# `show` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `show ip arp` — read-only

Dumps the router's ARP cache as a formatted text table.

**RCI** `/rci/show/ip/arp`

**Catch:** the IP column is not a unique key — the example carries `192.168.75.203` twice against two different MAC addresses, so code that indexes this by address will silently drop entries. Index by the pair instead.

**Returns (text table columns):** `IP`, `MAC`, `Interface`.

### `show ip conntrack lockout` — read-only

Reports conntrack lockout status and usage.

**RCI** `/rci/show/ip/conntrack/lockout`

**Catch:** the synopsis names a different command, `ip hotspot lockout`, even though the documented command and example are `ip conntrack lockout`; use the heading and example command rather than the synopsis when constructing the CLI call.

**Returns (fields):** `enabled`, `active`, `time-left`, `max-size`, `usage`, `public`.

### `show ip dhcp bindings` — read-only

Lists the DHCP leases currently issued by the selected pool or pools.

**RCI** `/rci/show/ip/dhcp/bindings`

**Catch:** each lease is emitted under the repeated `lease` key, with its `hostname` alongside it, so the response is a sequence of records rather than a map keyed by IP, MAC, or hostname.

**Arguments:**

| Argument | Notes |
|---|---|
| `pool` | Names the DHCP pool whose bindings are requested. |

**Returns (fields):** `lease`, `ip`, `mac`, `expires`, `hostname`.

### `show ip dhcp pool` — read-only

Reports the configuration and state of a DHCP pool.

**RCI** `/rci/show/ip/dhcp/pool`

**Catch:** NONE

**Returns (fields):** `pool`, `name`, `interface`, `binding`, `network`, `begin`, `end`, `router`, `default`, `lease`, `state`, `debug`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `pool` | String | — |

### `show ip ftp` — read-only

Reports the FTP server’s global and per-user home-directory settings.

**RCI** `/rci/show/ip/ftp`

**Catch:** `root` and `path` appear at two levels: once for the server and again inside each `user, index = N` record. In the example both levels hold the same value, so a parser that flattens by field name will silently conflate the global home directory with a user's.

**Returns (fields):** `enabled`, `permissive`, `root`, `path`, `user`, `index`, `name`.

### `show ip hotspot` — read-only

Lists hosts known to the hotspot service together with access, link, and wireless details.

**RCI** `/rci/show/ip/hotspot`

**Catch:** host records repeat under the same `host` key and include a nested `interface` record, so a consumer that stores one object per field name will overwrite earlier hosts or lose the interface association.

**Returns (fields):** `host`, `mac`, `via`, `ip`, `hostname`, `name`, `interface`, `id`, `description`, `expires`, `registered`, `access`, `schedule`, `active`, `rxbytes`, `txbytes`, `uptime`, `link`, `ssid`, `ap`, `authenticated`, `txrate`, `ht`, `mode`, `gi`, `rssi`, `mcs`.

### `show ip hotspot rrd` — read-only

Provides historical traffic samples for one registered host.

**RCI** `/rci/show/ip/hotspot/rrd`

**Catch:** NONE

**Returns (fields):** `data`, `t`, `v`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `mac` | MAC address | — |
| `attribute` | `rxspeed`, `txspeed`, `rxbytes`, or `txbytes` | — |
| `detail` | Integer | The documented values select different sampling intervals. |

### `show ip hotspot summary` — read-only

Summarizes Round Robin Database traffic for registered hosts in descending order.

**RCI** `/rci/show/ip/hotspot/summary`

**Catch:** the host order is part of the result: it is sorted descending, so a caller should not treat record position as a stable host identity. The timestamp also changes with detail; the examples show `t: 255` for the default and count-limited calls but `t: 0` for detail `0`.

**Returns (fields):** `t`, `host`, `active`, `name`, `rxspeed`, `txspeed`, `rxbytes`, `txbytes`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `attribute` | `rxspeed`, `txspeed`, `rxbytes`, or `txbytes` | — |
| `detail` | Integer | Selects the documented aggregation interval. |
| `count` | Integer | Limits the number of hosts returned. |

### `show ip http proxy` — read-only

Reports the configured HTTP proxy status.

**RCI** `/rci/show/ip/http/proxy`

**Catch:** NONE

**Returns (fields):** `proxy`, `name`, `domain`, `upstream`, `allow`, `ndns`.

### `show ip http webdav` — read-only

Reports WebDAV server settings and its indexed users.

**RCI** `/rci/show/ip/http/webdav`

**Catch:** the global root and path do not imply that every user has an override: in the example user index `0` has empty `root` and `path`, while user index `1` has explicit values.

**Returns (fields):** `enabled`, `permissive`, `root`, `path`, `user`, `index`, `name`.

### `show ip name-server` — read-only

Lists configured IPv4 and IPv6 DNS servers in priority order.

**RCI** `/rci/show/ip/name-server`

**Catch:** priority is conveyed by record order rather than a dedicated priority field; preserve the returned sequence when interpreting which server is preferred. The example also includes both IPv4 and IPv6 records.

**Returns (fields):** `server`, `address`, `port`, `domain`, `global`, `service`, `interface`.

### `show ip nat` — read-only

Presents the current network-address-translation sessions and packet counts.

**RCI** `/rci/show/ip/nat`

**Catch:** this is a ruled text table, not a key-value response, and one logical translation is shown across paired inbound/outbound lines; the `tcp` switch filters the records by protocol but does not change that two-line presentation.

**Arguments:**

| Argument | Notes |
|---|---|
| `tcp` | Restricts the displayed records to TCP. |

**Returns (text table columns):** `Type`, `In`, `Out`, `Source`, `Port`, `Destination`, `Port`, `Packets`.

### `show ip neighbour` — read-only

Lists discovered network-layer neighbors, optionally restricted to active hosts.

**RCI** `/rci/show/ip/neighbour`

**Catch:** the record shape depends on address family: the IPv4 example has one scalar `address`, while the IPv6 record nests one or more addresses under `addresses`, each with its own `status` and `last-seen`.

**Returns (fields):** `neighbour`, `id`, `via`, `mac`, `address-family`, `address`, `addresses`, `status`, `interface`, `first-seen`, `last-seen`, `leasetime`, `expired`, `wireless`.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `alive` | Keyword | Restricts the result to active hosts. |

### `show ip policy` — read-only

Reports IP policy profiles and the routes associated with each profile.

**RCI** `/rci/show/ip/policy`

**Catch:** profiles and routes are repeated records, and the example's targeted `Policy0` output omits the description shown in the unfiltered profile listing; code should therefore tolerate both the profile-list and selected-profile shapes.

**Arguments:**

| Argument | Notes |
|---|---|
| `policy` | Selects an IP Policy profile by name. |

**Returns (fields):** `policy`, `name`, `description`, `mark`, `table`, `route`, `destination`, `gateway`, `interface`, `metric`, `proto`, `floating`.

### `show ip route` — read-only

Prints the current routing table, optionally selecting a table and sorting its records.

**RCI** `/rci/show/ip/route`

**Catch:** the result is formatted text rather than API fields: the header presents `F Metric` as a wrapped table label, and sorted output is still a display table, not a JSON object keyed by destination.

**Arguments:**

| Argument | Notes |
|---|---|
| `table` | Supplies the route-table number. |
| `criteria` | May be `interface`, `gateway`, or `destination`. |
| `direction` | May be `ascending` or `descending`. |

**Returns (text table columns):** `Destination`, `Gateway`, `Interface`, `F`, `Metric`.

### `show ip service` — read-only

Lists the ports opened by system services.

**RCI** `/rci/show/ip/service`

**Catch:** `service-name` is not unique: the example repeats DNS proxy entries for different protocol/port combinations, so identify a row by more than the service name.

**Returns (fields):** `service`, `service-name`, `family`, `protocol`, `port`, `security-level`.
