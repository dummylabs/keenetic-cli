# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface mac access-list address` — changes settings

Adds a MAC address to the interface's permit or deny ACL.

**RCI** `/rci/interface/mac/access-list/address`

**Catch:** positive invocations add entries to the existing ACL, so configuring one address does not replace addresses previously added.


**Arguments:**

| Argument | Notes |
|---|---|
| `address` | The MAC address to add to the ACL. |

### `interface mac access-list type` — changes settings

Chooses whether the interface MAC ACL permits or denies listed addresses.

**RCI** `/rci/interface/mac/access-list/type`

**Catch:** `none` is an explicit selectable ACL type, not a `no`-form reset; this command has no `no` form.

**Arguments:**

| Argument | Notes |
|---|---|
| `type` | `none` leaves the filtering type undefined, `permit` admits listed MAC addresses, and `deny` restricts listed MAC addresses. |

### `interface mac address` — changes settings

Assigns a MAC address to a network interface or restores its original address.

**RCI** `/rci/interface/mac/address`

**Catch:** Wi-Fi interface changes are prohibited; on permitted interfaces the block allows arbitrary values but warns when the multicast bit is set or the OUI-enforced bit is clear.

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | The replacement MAC address. |

### `interface mac address factory` — changes settings

Assigns one of the router's factory MAC addresses to the selected interface.

**RCI** `/rci/interface/mac/address/factory`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Selects the factory address source: `lan`, `wan`, or `wlan5`. |

### `interface mac band` — changes settings

Binds a registered host to either the 2.4 GHz or the 5 GHz band.

**RCI** `/rci/interface/mac/band`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of the registered client. |
| `band` | `0` selects 2.4 GHz and `1` selects 5 GHz. |

**Catch:** the example assigns the same MAC first to band `0` and then to band `1`, which reads as a single binding being moved rather than two simultaneous bindings; verify this if a client is expected on both bands.

**Blast radius:** bare `no mac band` unbinds every host.

### `interface mac bssid` — changes settings

Sets the WISP access point BSSID to which a station interface should connect.

**RCI** `/rci/interface/mac/bssid`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `bssid` | The WISP access point's MAC address. |

### `interface mac clone` — changes settings

Copies the operator PC's MAC address to the selected interface.

**RCI** `/rci/interface/mac/clone`

**Catch:** the source address is the operator's PC address, not a value supplied as a command argument.

### `interface mac vht40` — changes settings

Adds a host MAC address to the Wi-Fi VHT40 compatibility list.

**RCI** `/rci/interface/mac/vht40`

**Arguments:**

| Argument | Notes |
|---|---|
| `vht40` | MAC address of the host to place in the compatibility list. |

**Catch:** the example's removal command names `fa:8e:80:ec:58:e2`, but its confirmation names the previously added `fa:8e:80:ec:12:11`; the capture is internally inconsistent, so do not rely on that confirmation to identify the removed host.

**Blast radius:** bare `no mac vht40` clears the entire compatibility list.
