# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip policy` — changes settings

Enters or creates a named IP Policy profile, with up to 64 profiles supported.

**RCI** `/rci/ip/policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Up to 32 characters; Latin letters, digits, hyphens, and underscores are accepted. |

**Catch:** selecting a name that does not yet exist creates the profile rather than failing.

### `ip policy description` — changes settings

Assigns a description to the current IP Policy profile.

**RCI** `/rci/ip/policy/description`

**Arguments:**

| Argument | Notes |
|---|---|
| `description` | Up to 256 characters; Latin letters, digits, hyphens, and underscores are accepted. |

**Catch:** NONE

### `ip policy ipv6 route` — changes settings

Adds an IPv6 static route to the selected IP Policy.

**RCI** `/rci/ip/policy/ipv6/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `prefix` | IPv6 destination prefix. |
| `interface` | Full interface name or alias used for the route. |
| `gateway` | Address of a router on a directly connected network. |
| `auto` | Makes the route apply when the specified gateway becomes available. |
| `metric` | Accepted but ignored by the current implementation. |
| `reject` | Pins traffic to the selected interface when used with `auto`; it cannot be used for the default route. |

**Catch:** `metric` has no effect. The `reject` option is valid only together with `auto` and is unavailable for the default route; additionally, the example reports a different displayed prefix for the `auto reject` invocation than for the same prefix without those options, which the block does not explain.

### `ip policy multipath` — changes settings

Enables simultaneous use of WAN connections in balancing mode for the current IP Policy.

**RCI** `/rci/ip/policy/multipath`

**Catch:** NONE

### `ip policy permit` — changes settings

Permits an IP Policy for a global interface, with an optional priority among global interfaces.

**RCI** `/rci/ip/policy/permit`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full interface name or alias. |
| `order` | Priority from 1 through 65534, but not above the number of global interfaces. |

**Catch:** the example submits `order 0` even though the argument description specifies a minimum of 1, so do not infer from that capture that zero is valid.

**Blast radius:** bare `no permit` denies the policy for every global interface.

### `ip policy permit auto` — changes settings

Permits new connections for the current IP Policy automatically.

**RCI** `/rci/ip/policy/permit/auto`

**Catch:** NONE

### `ip policy rate-limit input` — changes settings

Configures ingress rate limiting on a global interface for policy assignees.

**RCI** `/rci/ip/policy/rate-limit/input`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Global IP interface whose traffic is limited for policy assignees. |
| `rate` | Ingress limit from 64 to 1,000,000 kbps. |
| `auto` | Selects automatic ingress limiting. |

**Catch:** NONE

### `ip policy rate-limit output` — changes settings

Configures output rate limiting on a global interface for policy assignees.

**RCI** `/rci/ip/policy/rate-limit/output`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Global IP interface whose traffic is limited for policy assignees. |
| `rate` | Documented range is 64 to 1,000,000 kbps. |
| `auto` | Selects automatic limiting. |

**Catch:** NONE

### `ip policy route` — changes settings

Adds an IPv4 static route to the routing table for the current IP Policy.

**RCI** `/rci/ip/policy/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `network` | Destination network address used with `mask`. |
| `mask` | Destination network mask, in canonical or prefix-length form. |
| `host` | Destination node address for a host route. |
| `interface` | Full interface name or alias; on a point-to-point link it can identify the packet direction without another address. |
| `gateway` | Router address on a directly connected network; it may be paired with an interface to select global-interface priority. |
| `auto` | Makes the route apply when the gateway becomes available. |
| `metric` | Accepted but ignored by the current implementation. |
| `reject` | Pins traffic to the selected interface when used with `auto`; it cannot be used for the default route. |

**Catch:** `metric` has no effect, and `reject` is usable only with `auto` and not for the default route.

### `ip policy standalone` — changes settings

Enables standalone mode for the selected IP Policy profile.

**RCI** `/rci/ip/policy/standalone`

**Catch:** in standalone mode, static routes through interfaces marked global are not automatically copied from the main settings into this policy profile.
