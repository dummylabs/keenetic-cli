# `ping-check` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ping-check profile` — changes settings

Selects a Ping Check profile, creating it when it does not already exist.

**RCI** `/rci/ping-check/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Ping Check profile name; available names can be discovered with the command's completion list. |

**Catch:** entering a nonexistent profile name creates a new profile and enters its configuration context instead of reporting a missing-profile error.

### `ping-check profile host` — changes settings

Adds a hostname or address to the Ping Check profile's test targets.

**RCI** `/rci/ping-check/profile/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Name or address of the remote test host. |

**Catch:** each positive invocation adds a host to the profile, while the argument-free `no host` form clears the host list rather than removing only a default target.

### `ping-check profile max-fails` — changes settings

Sets the consecutive-failure threshold for declaring the Internet unavailable at the interface.

**RCI** `/rci/ping-check/profile/max-fails`

**Arguments:**

| Argument | Notes |
|---|---|
| `count` | Consecutive failed-request count from 1 through 10; the documented default is 5. |

**Catch:** the threshold is applied to consecutive failures and reaching it disables the interface; it is not a cumulative lifetime failure counter.

### `ping-check profile min-success` — changes settings

Sets the consecutive-success threshold for declaring the Internet available at the interface.

**RCI** `/rci/ping-check/profile/min-success`

**Arguments:**

| Argument | Notes |
|---|---|
| `count` | Consecutive successful-request count from 1 through 10; the documented default is 5. |

**Catch:** the threshold is applied to consecutive successes and reaching it enables the interface; it is not a cumulative success counter.

### `ping-check profile mode` — changes settings

Selects how the Ping Check profile tests remote-host availability.

**RCI** `/rci/ping-check/profile/mode`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `icmp` sends ICMP echo requests, `connect` establishes TCP, `tls` establishes TLS, and `uri` checks a URI; the documented default is `icmp`. |

**Catch:** NONE

### `ping-check profile port` — changes settings

Sets the remote port used for Ping Check connection tests.

**RCI** `/rci/ping-check/profile/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | Port number from 1 through 65534. |

**Catch:** the configured port is meaningful only when the profile uses `connect` mode; the block does not say that other modes consume or validate it.

### `ping-check profile power-cycle` — changes settings

Controls USB network-interface power-cycling for a Ping Check profile.

**RCI** `/rci/ping-check/profile/power-cycle`

**Catch:** The example shows two consecutive positive invocations changing the profile from enabled USB power cycle to disabled USB power cycle, so the positive form appears to toggle rather than simply enable; the block does not explain that behavior.

### `ping-check profile timeout` — changes settings

Sets the maximum response time for one remote-host request.

**RCI** `/rci/ping-check/profile/timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Response time in seconds, from 1 through 10; the documented default is 2 seconds. |

**Catch:** The argument-free `no timeout` form restores the documented 2-second default rather than disabling the check.

### `ping-check profile update-interval` — changes settings

Sets the period between Ping Check operations.

**RCI** `/rci/ping-check/profile/update-interval`

**Arguments:**

| Argument | Notes |
|---|---|
| `seconds` | Refresh period from 3 through 3600 seconds. |

**Catch:** NONE

### `ping-check profile uri` — changes settings

Adds a remote HTTP or HTTPS host to the Ping Check profile's URI targets.

**RCI** `/rci/ping-check/profile/uri`

**Arguments:**

| Argument | Notes |
|---|---|
| `uri` | Hostname or address of a remote HTTP or HTTPS host. |

**Catch:** Positive invocations accumulate URI targets—the example adds two distinct URIs—while the example's argumented `no uri <uri>` reports `URIs cleared`, so do not assume that removal is limited to the named URI; the block does not explain the scope.

**Blast radius:** The bare `no uri` is also shown reporting `URIs cleared`; treat it as potentially clearing the whole URI set rather than one target, pending verification.
