# `access-list` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `access-list` — changes settings

Creates or selects an ACL context for packet-filtering rules.

**RCI** `/rci/access-list`

**Catch:** if the named list does not exist, invoking the command creates it rather than failing; the `no` form removes the list and all rules it contains.

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | ACL name used for the packet-filtering rules list. |

### `access-list auto-delete` — changes settings

Controls whether ACL rules are removed automatically when an interface is deleted.

**RCI** `/rci/access-list/auto-delete`

**Catch:** the setting is forced on for ACLs whose names start with `_WEBADMIN_`; enabling it is rejected when the ACL has no bound interfaces, except while reading startup-config.

### `access-list deny` — changes settings

Adds or removes a packet-filtering rule that denies matching traffic.

**RCI** `/rci/access-list/deny`

**Arguments:**

| Argument | Notes |
|---|---|
| `tcp` | Selects TCP traffic. |
| `udp` | Selects UDP traffic. |
| `icmp` | Selects ICMP traffic. |
| `esp` | Selects ESP traffic. |
| `gre` | Selects GRE traffic. |
| `ipip` | Selects IP-in-IP traffic. |
| `ip` | Matches IP traffic, including TCP, UDP, ICMP, and other IP protocols. |
| `source` | Address compared against the packet's source address. |
| `source-mask` | Mask applied before comparing the source; canonical and prefix-length forms are accepted. |
| `source-port` | TCP or UDP source port used by a port comparison or range. |
| `source-end-port` | Upper endpoint of a source-port range. |
| `src-port-operator` | Source-port comparison operator: `lt`, `eq`, or `gt`. |
| `destination` | Address compared against the packet's destination address. |
| `destination-mask` | Mask applied before comparing the destination; canonical and prefix-length forms are accepted. |
| `destination-port` | TCP or UDP destination port used by a port comparison or range. |
| `destination-end-port` | Upper endpoint of a destination-port range. |
| `dst-port-operator` | Destination-port comparison operator: `lt`, `eq`, or `gt`. |

**Catch:** port clauses are available only in the TCP and UDP forms; the ICMP, ESP, GRE, IP-in-IP, and generic IP forms accept only the address and mask pair.

### `access-list permit` — changes settings

Adds or removes a packet-filtering rule that permits matching traffic.

**RCI** `/rci/access-list/permit`

**Arguments:**

| Argument | Notes |
|---|---|
| `tcp` | Selects TCP traffic. |
| `udp` | Selects UDP traffic. |
| `icmp` | Selects ICMP traffic. |
| `esp` | Selects ESP traffic. |
| `gre` | Selects GRE traffic. |
| `ipip` | Selects IP-in-IP traffic. |
| `ip` | Matches IP traffic, including TCP, UDP, ICMP, and other IP protocols. |
| `source` | Address compared against the packet's source address. |
| `source-mask` | Mask applied before comparing the source; canonical and prefix-length forms are accepted. |
| `source-port` | TCP or UDP source port used by a port comparison or range. |
| `source-end-port` | Upper endpoint of a source-port range. |
| `src-port-operator` | Source-port comparison operator: `lt`, `eq`, or `gt`. |
| `destination` | Address compared against the packet's destination address. |
| `destination-mask` | Mask applied before comparing the destination; canonical and prefix-length forms are accepted. |
| `destination-port` | TCP or UDP destination port used by a port comparison or range. |
| `destination-end-port` | Upper endpoint of a destination-port range. |
| `dst-port-operator` | Destination-port comparison operator: `lt`, `eq`, or `gt`. |

**Catch:** port clauses are available only in the TCP and UDP forms; the ICMP, ESP, GRE, IP-in-IP, and generic IP forms accept only the address and mask pair.

### `access-list rule` — changes settings

Adjusts an ACL rule's enabled state, schedule, position, or description.

**RCI** `/rci/access-list/rule`

**Arguments:**

| Argument | Notes |
|---|---|
| `index` | ACL rule number. |
| `disable` | Selects the rule-disable operation. |
| `schedule` | Binds a schedule created through the schedule command group. |
| `order` | Supplies the rule's new position in the list. |
| `description` | Text assigned to the ACL rule. |

**Catch:** the `no` synopsis has branches for `disable`, `schedule`, and `description`, but none for `order`, so reordering has no corresponding `no` branch.
