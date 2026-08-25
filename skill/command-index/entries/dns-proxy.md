# `dns-proxy` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `dns-proxy` — read-only

Enters the command group for managing the DNS proxy service.

**RCI** `/rci/dns-proxy`

**Catch:** NONE

### `dns-proxy debug` — changes settings

Controls debug mode for the DNS proxy service.

**RCI** `/rci/dns-proxy/debug`

**Catch:** NONE

### `dns-proxy filter assign host preset` — changes settings

Associates a filtering preset with a particular network device.

**RCI** `/rci/dns-proxy/filter/assign/host/preset`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | The device is identified by MAC address. |
| `preset` | The preset name must come from the router's available preset list. |

**Catch:** host assignments are removed with a host-specific form, but the empty-argument form operates on all host preset assignments.

**Blast radius:** bare `no filter assign host preset` removes presets for every host.

### `dns-proxy filter assign host profile` — changes settings

Associates a filtering profile with a particular network device.

**RCI** `/rci/dns-proxy/filter/assign/host/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | The device is identified by MAC address. |
| `profile` | The profile name must be an existing user-defined profile. |

**Catch:** a host-specific removal and a global removal use the same command family, with the distinction made solely by whether the host argument is present.

**Blast radius:** bare `no filter assign host profile` removes profiles for every host.

### `dns-proxy filter assign interface preset` — changes settings

Applies a filtering preset to devices on an interface segment unless they already have a profile or preset.

**RCI** `/rci/dns-proxy/filter/assign/interface/preset`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Must have a private or protected security level. |
| `preset` | The preset name must come from the router's available preset list. |

**Catch:** this is a fallback assignment for the segment, not an unconditional overwrite: devices with an existing profile or preset are excluded.

**Blast radius:** bare `no filter assign interface preset` clears preset assignments for all interfaces.

### `dns-proxy filter assign interface profile` — changes settings

Applies a filtering profile to devices on an interface segment that lack an existing profile or preset.

**RCI** `/rci/dns-proxy/filter/assign/interface/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Must have a private or protected security level. |
| `profile` | The profile name must be an existing user-defined profile. |

**Catch:** the segment assignment deliberately skips devices that already have either kind of filtering assignment, so it is not a force-overwrite operation.

**Blast radius:** bare `no filter assign interface profile` clears profile assignments for all interfaces.

### `dns-proxy filter engine` — changes settings

Selects the DNS filtering engine or disables filtering.

**RCI** `/rci/dns-proxy/filter/engine`

**Arguments:**

| Argument | Notes |
|---|---|
| `engine` | One of `interceptor`, `public`, `nextdns`, `opkg`, or `skydns`. |

**Catch:** disabling the filter engine makes the corresponding value in a config request empty rather than leaving the previous engine name visible.

### `dns-proxy filter profile` — changes settings

Creates or removes a custom DNS filtering profile.

**RCI** `/rci/dns-proxy/filter/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Reduced-form profile name, limited to 32 characters; no more than 8 profiles may exist. |

**Catch:** the profile namespace is capped at 8 profiles, so a syntactically valid new name can still fail once that limit is reached.

### `dns-proxy filter profile description` — changes settings

Assigns or clears the description associated with a DNS filtering profile.

**RCI** `/rci/dns-proxy/filter/profile/description`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Name of the profile whose description is targeted. |
| `description` | Arbitrary profile-description text. |

**Catch:** clearing the description uses the `no` form with the profile name and no description value, despite the synopsis displaying a description placeholder on that form.

### `dns-proxy filter profile dns53 upstream` — changes settings

Adds an ordinary DNS server to a user-defined filtering profile.

**RCI** `/rci/dns-proxy/filter/profile/dns53/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Selects the user-defined profile being edited. |
| `address` | Server address. |
| `port` | Optional server port. |

**Catch:** a profile can contain at most six of these servers, and the block's displayed no-form says `description` where the examples use `upstream`; treat that synopsis spelling as inconsistent.

**Blast radius:** omitting the server arguments from the no-form removes the profile's whole DNS-server list.

### `dns-proxy filter profile https upstream` — changes settings

Adds a DNS-over-HTTPS service to a user-defined filtering profile.

**RCI** `/rci/dns-proxy/filter/profile/https/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Selects the user-defined profile being edited. |
| `url` | Identifies the DNS-over-HTTPS service. |
| `hash` | Optional certificate pinning value supplied with `spki`. |

**Catch:** no more than six servers can be stored in one profile, and the shown no-form uses `description` instead of `upstream` even though the examples use `upstream`.

**Blast radius:** omitting the URL from the no-form removes the profile's entire DNS-over-HTTPS server list.

### `dns-proxy filter profile intercept enable` — changes settings

Controls interception of transit DNS requests for a named filtering profile.

**RCI** `/rci/dns-proxy/filter/profile/intercept/enable`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Filtering profile whose transit-DNS interception setting is changed. |

**Catch:** NONE

### `dns-proxy filter profile tls upstream` — changes settings

Adds a DNS-over-TLS service to a user-defined filtering profile.

**RCI** `/rci/dns-proxy/filter/profile/tls/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Selects the user-defined profile being edited. |
| `address` | The server may be specified by an IP address or an FQDN. |
| `port` | Optional server port. |
| `fqdn` | SNI name supplied after `sni`. |
| `hash` | Certificate pinning value supplied after `spki`. |

**Catch:** each profile is limited to six servers, and the displayed no-form contains `description` instead of `upstream`; the examples use `upstream`.

**Blast radius:** omitting the address and port from the no-form removes the profile's entire DNS-over-TLS server list.

### `dns-proxy https upstream` — changes settings

Registers a DNS-over-HTTPS upstream for the router's secure DNS service.

**RCI** `/rci/dns-proxy/https/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `url` | Custom DNS service URL. |
| `format` | Selects the `dnsm` or `json` representation. |
| `hash` | Certificate pinning value supplied with the `sni` option shown in the syntax. |
| `interface` | Optional interface restriction supplied after `on`. |
| `domain` | Optional domain association. |

**Catch:** the example adds the same AdGuard URL once without an interface and once with `on ISP`, so URL alone is not necessarily a unique identity for a configured upstream.

**Blast radius:** bare `no https upstream` deletes every configured DNS-over-HTTPS upstream.

### `dns-proxy intercept enable` — changes settings

Controls interception of transit DNS requests for the system filtering profile.

**RCI** `/rci/dns-proxy/intercept/enable`

**Catch:** NONE

### `dns-proxy max-ttl` — changes settings

Sets or clears the maximum lifetime of cached DNS entries.

**RCI** `/rci/dns-proxy/max-ttl`

**Arguments:**

| Argument | Notes |
|---|---|
| `max-ttl` | Maximum cached-entry TTL in milliseconds, from 1 through 604800000. |

**Catch:** the `no` form clears the maximum-TTL setting instead of taking another numeric value.

### `dns-proxy proceed` — changes settings

Sets the interval used between concurrent DNS-proxy requests sent to multiple DNS servers.

**RCI** `/rci/dns-proxy/proceed`

**Arguments:**

| Argument | Notes |
|---|---|
| `proceed` | Interval in milliseconds, from 1 through 50000. |

**Catch:** the `no` form restores the documented default of 500 milliseconds rather than disabling the interval.

### `dns-proxy rebind-protect` — changes settings

Selects the DNS rebinding protection mode.

**RCI** `/rci/dns-proxy/rebind-protect`

**Arguments:**

| Argument | Notes |
|---|---|
| `auto` | Blocks responses pointing to addresses in private network segments. |
| `strict` | Blocks responses pointing to subnets listed in the IANA IPv4 Special-Purpose Address Registry. |

**Catch:** `auto` and `strict` use different blocklists: private network segments versus the IANA special-purpose subnet list.

### `dns-proxy route object-group` — changes settings

Creates a DNS route whose destinations come from an FQDN object group.

**RCI** `/rci/dns-proxy/route/object-group`

**Arguments:**

| Argument | Notes |
|---|---|
| `group` | Names the FQDN object group. |
| `gateway` | May be IPv4 or IPv6; it can be paired with `interface`, or the interface alone can be used. |
| `interface` | Can be a full interface name or an alias; it is also the selector used by the no-form. |
| `auto` | Makes installation depend on the gateway becoming available. |
| `reject` | Valid only together with `auto`, and not for the default route; it prevents fallback to other routes when the selected interface is inactive. |

**Catch:** repeated calls for `domain-list0` are reported as updates after the first add, so changing gateway or flags modifies the existing object-group route rather than creating an independent sibling; the `reject` option is additionally constrained to `auto` and non-default routes.

**Blast radius:** bare `no route` clears every DNS route, not only object-group routes.

### `dns-proxy srr-reset` — changes settings

Sets the DNS proxy send-response rating reset interval in milliseconds.

**RCI** `/rci/dns-proxy/srr-reset`

**Arguments:**

| Argument | Notes |
|---|---|
| `srr-reset` | Reset interval in milliseconds; accepted values are 0–600000, with 600000 as the documented default. |

**Catch:** the `no` form restores the documented default interval rather than disabling the reset mechanism.

### `dns-proxy tls upstream` — changes settings

Registers a DNS-over-TLS upstream for the router's secure DNS service.

**RCI** `/rci/dns-proxy/tls/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Address of the DNS-over-TLS server. |
| `port` | Server port. |
| `fqdn` | SNI name supplied after `sni`. |
| `hash` | Certificate pinning value supplied after `spki`. |
| `interface` | Optional interface restriction supplied after `on`. |
| `domain` | Optional domain association. |

**Catch:** the example registers `1.1.1.1:853` both without an interface and with `on ISP`, showing that address and port alone need not identify a unique upstream.

**Blast radius:** bare `no tls upstream` deletes every configured DNS-over-TLS upstream.
