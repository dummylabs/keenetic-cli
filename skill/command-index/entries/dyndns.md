# `dyndns` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `dyndns profile` — changes settings

Selects a DynDNS profile, creating it when the named profile is absent.

**RCI** `/rci/dyndns/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Profile name, up to 64 characters. |

**Catch:** a nonexistent profile name is created instead of rejected, and the manual limits the device to 32 profiles.

### `dyndns profile domain` — changes settings

Assigns the permanent domain name used by the selected DynDNS profile.

**RCI** `/rci/dyndns/profile/domain`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Domain name, up to 254 characters. |

**Catch:** the domain must already be registered with dyndns.com or no-ip.com; this command does not perform that registration.

### `dyndns profile password` — changes settings

Stores the password used when the selected DynDNS profile authenticates.

**RCI** `/rci/dyndns/profile/password`

**Arguments:**

| Argument | Notes |
|---|---|
| `password` | Authentication password, up to 64 characters. |

**Catch:** NONE

### `dyndns profile send-address` — changes settings

Controls whether the connection IP address is included in a DynDNS request.

**RCI** `/rci/dyndns/profile/send-address`

**Catch:** NONE

### `dyndns profile type` — changes settings

Chooses the DynDNS provider type for the selected profile.

**RCI** `/rci/dyndns/profile/type`

**Arguments:**

| Argument | Notes |
|---|---|
| `type` | Provider selector: `dyndns`, `noip`, `opendns`, `dnsomatic`, `anydns`, `dnshome`, `duckdns`, `dyndnsfree`, `desec`, or `custom`. |

**Catch:** the `custom` choice depends on a service URL configured through `dyndns profile url`; it is not a complete provider selection by itself.

### `dyndns profile update-interval` — changes settings

Sets how often the selected DynDNS profile updates its address.

**RCI** `/rci/dyndns/profile/update-interval`

**Arguments:**

| Argument | Notes |
|---|---|
| `days` | Number of whole days in the interval. |
| `hours` | Number of whole hours in the interval. |
| `minutes` | Number of whole minutes in the interval. |
| `seconds` | Number of whole seconds in the interval. |

**Catch:** the example shows that a days-only form is accepted and normalized to seconds, so all four unit arguments are not required together.

### `dyndns profile url` — changes settings

Stores the custom dynamic-DNS service URL for the selected profile.

**RCI** `/rci/dyndns/profile/url`

**Arguments:**

| Argument | Notes |
|---|---|
| `url` | URL of the custom DNS service. |

**Catch:** NONE

### `dyndns profile username` — changes settings

Stores the username used when the selected DynDNS profile authenticates.

**RCI** `/rci/dyndns/profile/username`

**Arguments:**

| Argument | Notes |
|---|---|
| `username` | Authentication username, up to 64 characters. |

**Catch:** NONE
