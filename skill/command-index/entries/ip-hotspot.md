# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip hotspot` — read-only

Enters the command group for Hotspot configuration.

**RCI** `/rci/ip/hotspot`

**Catch:** NONE

### `ip hotspot auto-register disable` — changes settings

Controls automatic host registration in the Home segment, which starts enabled.

**RCI** `/rci/ip/hotspot/auto-register/disable`

**Catch:** the command's positive form is the disabling operation, while its `no` form re-enables automatic registration.

### `ip hotspot auto-scan interface` — changes settings

Controls passive subnetwork scanning separately for each interface.

**RCI** `/rci/ip/hotspot/auto-scan/interface`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full interface name or alias whose scanning setting is changed. |

**Catch:** the example is internally inconsistent: it shows the same positive command followed first by an “unchanged” message and then by a “disabled” message, so it does not establish toggle behavior; use the documented `no` form for disabling.

### `ip hotspot auto-scan interval` — changes settings

Sets the interval, in seconds, between probes of online hosts, defaulting to 30.

**RCI** `/rci/ip/hotspot/auto-scan/interval`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | Probe interval in seconds. |

**Catch:** NONE

### `ip hotspot auto-scan passive` — changes settings

Sets the passive autoscan rate, defaulting to three hosts per second.

**RCI** `/rci/ip/hotspot/auto-scan/passive`

**Arguments:**

| Argument | Notes |
|---|---|
| `rate` | Passive scan rate; the synopsis requires the literal `hps` suffix. |

**Catch:** `hps` is part of the command syntax after the rate, so a caller must include that literal unit token rather than send only the numeric rate.

### `ip hotspot auto-scan timeout` — changes settings

Sets how long an absent host may remain in the online-host list, defaulting to 35 seconds.

**RCI** `/rci/ip/hotspot/auto-scan/timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Offline timeout in seconds. |

**Catch:** expiry removes the missing host from the online-host list; it is not merely a status update that leaves the host listed.

### `ip hotspot default-policy` — changes settings

Sets the fallback Hotspot access rule for interfaces or an IP Policy profile, defaulting to permit.

**RCI** `/rci/ip/hotspot/default-policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `access` | Either `permit` or `deny` for internet access. |
| `policy` | Name of an IP Policy profile. |

**Catch:** the default applies only to hosts without an explicit access rule, so a host-specific rule takes precedence over this setting.

### `ip hotspot host` — changes settings

Assigns an access, schedule, or IP Policy rule to a particular Hotspot client.

**RCI** `/rci/ip/hotspot/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of a host that has already been registered with `known host`. |
| `access` | Either `permit` or `deny` for internet access. |
| `schedule` | Name of a schedule created by the schedule-group commands. |
| `policy` | Name of an IP Policy profile. |

**Catch:** the client must already be registered before this rule can be applied, and the resulting host rule overrides the interface-based Hotspot policy.

### `ip hotspot host conform` — changes settings

Assigns the segment-default policy to a registered host.

**RCI** `/rci/ip/hotspot/host/conform`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of the host. |

**Catch:** this applies to registered hosts, so the host must first be added through `known host`.

### `ip hotspot host priority` — changes settings

Assigns a traffic priority to a registered Hotspot host.

**RCI** `/rci/ip/hotspot/host/priority`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of the host. |
| `priority` | `1` is top priority and `7` is low; `6` is the normal default. |

**Catch:** the host must be registered through `known host` before a host priority can be applied.

### `ip hotspot policy` — changes settings

Sets the fallback Hotspot policy for a particular interface, defaulting to permit.

**RCI** `/rci/ip/hotspot/policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full Ethernet interface name or alias. |
| `access` | Either `permit` or `deny` for internet access. |
| `policy` | Name of an IP Policy profile. |

**Catch:** the interface policy is used only for hosts without an explicit access rule; a host-specific rule overrides it.

### `ip hotspot priority` — changes settings

Assigns a traffic priority to all traffic bound to an interface.

**RCI** `/rci/ip/hotspot/priority`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full interface name or alias. |
| `priority` | `1` is top priority and `7` is low; `6` is the normal default. |

**Catch:** NONE

### `ip hotspot wake` — read-only

Sends a Wake-on-LAN packet for a host through the Hotspot facility.

**RCI** `/rci/ip/hotspot/wake`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of the target host. |

**Catch:** The packet is sent only through the host's private and protected interfaces, not to an unrestricted set of interfaces.
