# `object-group` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `object-group fqdn` — changes settings

Creates an object group with automatic FQDN resolution.

**RCI** `/rci/object-group/fqdn`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | FQDN object-group name. |

**Catch:** NONE

### `object-group fqdn exclude` — changes settings

Adds or removes an excluded element in an FQDN object group.

**RCI** `/rci/object-group/fqdn/exclude`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | IPv4 address, IPv6 address, prefix-length subnet, or domain name. |

**Catch:** despite the FQDN name, the element can be a whole IPv4 or IPv6 subnet such as `0.0.0.0/0` or `::/0`, not only a domain name.

**Blast radius:** bare `no exclude` clears the entire excluded-element list for the object group.

### `object-group fqdn include` — changes settings

Adds or removes an included element in an FQDN object group.

**RCI** `/rci/object-group/fqdn/include`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | IPv4 address, IPv6 address, prefix-length subnet, or domain name. |

**Catch:** despite the FQDN name, the element can be a whole IPv4 or IPv6 subnet such as `0.0.0.0/0` or `::/0`, not only a domain name.

**Blast radius:** bare `no include` clears the entire included-element list for the object group.

### `object-group ip` — changes settings

Creates an IPv4 object group for subnet and optional protocol or port-range entries.

**RCI** `/rci/object-group/ip`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | IPv4 object-group name. |

**Catch:** NONE

### `object-group ip exclude` — changes settings

Adds or removes a non-matching element in an IP object group.

**RCI** `/rci/object-group/ip/exclude`

**Arguments:**

| Argument | Notes |
|---|---|
| `proto` | Protocol selector: `ip`, `tcp`, `udp`, `tcpudp`, `icmp`, `esp`, `gre`, or `ipip`. |
| `address` | IPv4 address or prefix-length subnet. |
| `port` | TCP/UDP port; when absent, the entry covers all incoming requests according to the block. |
| `end-port` | End of the port range. |

**Catch:** NONE

### `object-group ip include` — changes settings

Adds or removes a matching element in an IP object group.

**RCI** `/rci/object-group/ip/include`

**Arguments:**

| Argument | Notes |
|---|---|
| `proto` | Protocol selector: `ip`, `tcp`, `udp`, `tcpudp`, `icmp`, `esp`, `gre`, or `ipip`. |
| `address` | IPv4 address or prefix-length subnet. |
| `port` | TCP/UDP port; when absent, the entry covers all incoming requests according to the block. |
| `end-port` | End of the port range. |

**Catch:** NONE
