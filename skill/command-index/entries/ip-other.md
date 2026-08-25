# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip arp` — changes settings

Installs a static IP-to-MAC association in the ARP table.

**RCI** `/rci/ip/arp`

**Arguments:**

| Argument | Notes |
|---|---|
| `ip` | IPv4 address written in four-part dotted-decimal form. |
| `mac` | Six colon-separated hexadecimal pairs. |

**Catch:** the no-form targets an entry by IP alone, while the add form supplies both IP and MAC; changing a mapping therefore means removing the old IP entry rather than selecting it by MAC.

**Blast radius:** bare `no ip arp` clears the complete static ARP table.

### `ip conntrack lockout disable` — changes settings

Turns off conntrack table protection, which the block says is on by default.

**RCI** `/rci/ip/conntrack/lockout/disable`

**Catch:** protection is enabled by default, so this command is an opt-out and the bare `no` form re-enables protection.

### `ip conntrack lockout duration` — changes settings

Sets how long conntrack lockout lasts.

**RCI** `/rci/ip/conntrack/lockout/duration`

**Arguments:**

| Argument | Notes |
|---|---|
| `duration` | Lockout duration from 60 through 3600 seconds; the default is 600 seconds. |

**Catch:** NONE

### `ip conntrack lockout threshold public` — changes settings

Sets the public-interface connection threshold as a fraction of the conntrack table.

**RCI** `/rci/ip/conntrack/lockout/threshold/public`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Percentage from 50 through 99 inclusive; the default is 80 percent. |

**Catch:** NONE

### `ip conntrack max-entries` — changes settings

Sets the maximum number of entries allocated for conntrack and NAT tracking.

**RCI** `/rci/ip/conntrack/max-entries`

**Arguments:**

| Argument | Notes |
|---|---|
| `max-entries` | Maximum number of table entries. |

**Catch:** there is no negated form for restoring or removing the configured table size.

### `ip conntrack sweep threshold` — changes settings

Sets the percentage at which waiting conntrack sessions start being cleaned up.

**RCI** `/rci/ip/conntrack/sweep/threshold`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | Percentage from 50 through 99 inclusive; the default is 70 percent. |

**Catch:** the synopsis shows a `no ... threshold duration` form, but the example uses `no ... threshold`; the block does not explain whether `duration` is a documentation error or a required token.

### `ip esp alg enable` — changes settings

Enables IPSec ESP passthrough.

**RCI** `/rci/ip/esp/alg/enable`

**Catch:** NONE

### `ip flow-cache timeout active` — changes settings

Sets the active-session cache timeout in minutes, with a default of 10.

**RCI** `/rci/ip/flow-cache/timeout/active`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Minutes, from 1 through 30. |

**Catch:** NONE

### `ip flow-cache timeout inactive` — changes settings

Sets the inactive-session cache timeout in seconds, with a default of 20.

**RCI** `/rci/ip/flow-cache/timeout/inactive`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Seconds, from 1 through 600. |

**Catch:** NONE

### `ip flow-export destination` — changes settings

Configures the NetFlow collector address and UDP port.

**RCI** `/rci/ip/flow-export/destination`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | IP address of the data collector. |
| `port` | UDP port; accepted values are 2055, 2056, 4432, 4739, 9025, 9026, 9995, 9996, and 6343. |

**Catch:** NONE

### `ip flow-export version` — changes settings

Selects the NetFlow export protocol version, defaulting to version 5.

**RCI** `/rci/ip/flow-export/version`

**Arguments:**

| Argument | Notes |
|---|---|
| `version` | Protocol version string. |

**Catch:** NONE

### `ip ftp` — read-only

Enters the command group for managing FTP access.

**RCI** `/rci/ip/ftp`

**Catch:** NONE

### `ip ftp client-charset` — changes settings

Sets the FTP server's default client character encoding, defaulting to UTF-8.

**RCI** `/rci/ip/ftp/client-charset`

**Arguments:**

| Argument | Notes |
|---|---|
| `charset` | One of: `utf-8`, `utf-16`, `utf-16le`, `utf-16be`, `utf-32`, `utf-32le`, `utf-32be`, `iso-8859-1` through `iso-8859-16`, `cp-037`, `cp-424`, `cp-437`, `cp-500`, `cp-737`, `cp-775`, `cp-850`, `cp-852`, `cp-855`, `cp-856`, `cp-857`, `cp-860`, `cp-861`, `cp-862`, `cp-863`, `cp-864`, `cp-865`, `cp-866`, `cp-869`, `cp-874`, `cp-1026`, `cp-1250` through `cp-1258`, `koi8-r`, `koi8-u`, `kz-1048`, `nextstep`, `mac-celtic`, `mac-centeuro`, `mac-croatian`, `mac-cyrillic`, `mac-gaelic`, `mac-greek`, `mac-icelandic`, `mac-inuit`, `mac-roman`, `mac-romanian`, `mac-turkish`, or `mac-ukrainian`. |

**Catch:** NONE

### `ip ftp lockout-policy` — changes settings

Configures FTP brute-force detection thresholds and timing.

**RCI** `/rci/ip/ftp/lockout-policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | Failed-login count; default 5, permitted range 3–20, or `0` for the reset operation. |
| `duration` | Authorization-ban duration in minutes; default 15, range 1–60. |
| `observation-window` | Suspicious-activity observation period in minutes; default 3, range 1–10. |

**Catch:** `0` is a sentinel on the threshold argument: it resets all brute-force detection parameters to their defaults rather than configuring a zero-attempt threshold.

### `ip ftp permissive` — changes settings

Allows FTP access without user authentication.

**RCI** `/rci/ip/ftp/permissive`

**Catch:** enabling this grants unauthenticated access to the FTP server for all users.

### `ip ftp security-level` — changes settings

Sets the interface-visibility level from which the FTP server accepts access.

**RCI** `/rci/ip/ftp/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Allows access from public, private, and protected interfaces. |
| `private` | Allows access from private interfaces only. |
| `protected` | Allows access from private and protected interfaces, but not public ones. |

**Catch:** the level names are not a simple cumulative permission scale: `public` permits all three interface classes, while `protected` excludes public interfaces and `private` excludes both public and protected interfaces.

### `ip host` — changes settings

Adds a static DNS record pairing a domain name with an IP address.

**RCI** `/rci/ip/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Domain name for the host record. |
| `address` | IP address paired with the domain. |

**Catch:** the example deletes a record by supplying both the domain and address; the block does not establish that a domain alone is a sufficient record key.

### `ip name-server` — changes settings

Configures static DNS server entries, optionally scoped by domain and interface.

**RCI** `/rci/ip/name-server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | DNS server IP address. |
| `port` | DNS server port. |
| `domain` | Domain matched by the DNS proxy; `""` denotes the default domain, and one entry can carry up to 16 domains. |
| `interface` | Interface on which the server entry is configured. |

**Catch:** changing a static entry makes the static servers active over dynamically learned servers until another dynamic registration occurs; repeated calls add separate server entries rather than replacing the list.

**Blast radius:** bare `no ip name-server` clears the entire static DNS-server list, while an argument-bearing form removes the specified entry from both static and active lists.

### `ip nat` — changes settings

Adds source-address translation for traffic from an interface or an explicitly supplied address range.

**RCI** `/rci/ip/nat`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full source-interface name or alias. |
| `address` | IP address used with `mask` to define the translation range. |
| `mask` | Translation-range mask, in canonical or prefix-length form. |

**Catch:** each positive invocation adds a NAT rule, so repeated commands accumulate rules rather than replace the existing NAT setup; interface-based and address-range rules are alternative forms, and the latter requires the `mask` companion argument.

### `ip nat full-cone` — changes settings

Controls Full Cone NAT mode.

**RCI** `/rci/ip/nat/full-cone`

**Catch:** NONE

### `ip nat oc` — changes settings

Controls NAT for OpenConnect VPN clients.

**RCI** `/rci/ip/nat/oc`

**Catch:** this command is available only when the OpenConnect VPN server component is installed.

### `ip nat restricted-cone` — changes settings

Controls Restricted NAT mode.

**RCI** `/rci/ip/nat/restricted-cone`

**Catch:** NONE

### `ip nat sstp` — changes settings

Controls NAT for SSTP VPN clients.

**RCI** `/rci/ip/nat/sstp`

**Catch:** this command is available only when the SSTP VPN server component is installed.

### `ip nat vpn` — changes settings

Enables translation for PPTP VPN clients.

**RCI** `/rci/ip/nat/vpn`

**Catch:** this command is available only when the PPTP VPN server component is installed.

### `ip route` — changes settings

Adds an IPv4 static route, including a route specified with the `default` keyword.

**RCI** `/rci/ip/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `network` | Destination network address used with `mask`. |
| `mask` | Destination network mask, in canonical or prefix-length form. |
| `host` | Destination node address for a host route. |
| `default` | Selects a default route. |
| `interface` | Full interface name or alias; a point-to-point interface can supply the packet direction without extra channel addressing. |
| `gateway` | Router address on a directly connected network; it may be paired with an interface to select global-interface priority. |
| `auto` | Makes the route apply when the gateway becomes available. |
| `metric` | Accepted but ignored by the current implementation. |
| `reject` | Pins traffic to the selected interface when used with `auto`; it cannot be used for the default route. |

**Catch:** `metric` has no effect, and `reject` is usable only with `auto` and not for the default route. The example's bare `no ip route default` reports no matching route after a default route was added via `Home`, so the block does not establish that the bare form removes that route.

### `ip search-domain` — changes settings

Assigns the search domain used for resolving non-fully-qualified hostnames.

**RCI** `/rci/ip/search-domain`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Domain name assigned to the resolver search setting. |

**Catch:** NONE

### `ip sip alg direct-media` — changes settings

Enables rewriting of the IP address in the Owner field of SDP for SIP traffic.

**RCI** `/rci/ip/sip/alg/direct-media`

**Catch:** the feature is intended to avoid configuring separate VoIP port forwarding; enabling it is not itself a port-forwarding rule.

### `ip sip alg port` — changes settings

Sets the SIP ALG message port, whose default is 5060.

**RCI** `/rci/ip/sip/alg/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | SIP message port; the no-form restores the default. |

**Catch:** NONE

### `ip static` — changes settings

Creates static NAT translations between global and local addresses and interfaces.

**RCI** `/rci/ip/static`

**Arguments:**

| Argument | Notes |
|---|---|
| `protocol` | One of `tcp`, `udp`, `icmp`, `tcpudp`, `gre`, or `ipip`. |
| `interface` | Input interface name or alias. |
| `comment` | User note introduced with `!`. |
| `address` + `mask` | Destination address range to translate; the mask accepts canonical or prefix-length form. |
| `port` | Incoming TCP/UDP destination port. |
| `end-port` | End of a translated port range. |
| `to-address` | Post-translation destination address. |
| `to-host` | Post-translation destination MAC; only known hosts are accepted. |
| `to-port` | Post-translation destination port. |
| `to-interface` | Interface used after translation. |

**Catch:** static NAT rules take priority over `ip nat` rules and open the specified port through the firewall automatically. A `to-host` rule is tied to the known host, so deleting that host also deletes the associated rule; the example also exposes a global `ip static disable` switch separate from adding a rule.

### `ip static rule` — changes settings

Disables a numbered static NAT rule or attaches a schedule to it.

**RCI** `/rci/ip/static/rule`

**Arguments:**

| Argument | Notes |
|---|---|
| `index` | Number identifying the translation rule. |
| `disable` | Marks the selected translation rule disabled. |
| `schedule` | Name of a schedule created by the schedule command group. |

**Catch:** the no-form has two distinct inverse effects: `no ... disable` enables the rule, while `no ... schedule` removes its schedule.

### `ip telnet` — read-only

Enters the command group for managing the Telnet server.

**RCI** `/rci/ip/telnet`

**Catch:** NONE

### `ip telnet lockout-policy` — changes settings

Configures Telnet brute-force detection thresholds and timing for public interfaces.

**RCI** `/rci/ip/telnet/lockout-policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | Failed-login threshold from 4 to 20; the documented default is 5. |
| `duration` | Ban duration from 1 to 60 minutes; the documented default is 15. |
| `observation-window` | Suspicious-activity window from 1 to 10 minutes; the documented default is 3. |

**Catch:** the description says `0` resets all brute-force parameters to defaults, but the example's `lockout-policy 0` message says only that detection is enabled; the block does not reconcile those two behaviors. The no-form disables detection.

### `ip telnet port` — changes settings

Sets the Telnet listening port and provides a reset form for the default port.

**RCI** `/rci/ip/telnet/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `number` | Port number from 1 through 65535. |

**Catch:** `no port` restores the documented default of port 23. The example reports `Port unchanged` after both setting and resetting, so that message is not confirmation of the requested port value.

### `ip telnet security-level` — changes settings

Controls which interface classes may reach the Telnet server.

**RCI** `/rci/ip/telnet/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Allows access from public, private, and protected interfaces. |
| `private` | Allows access from private interfaces. |
| `protected` | Allows access from private and protected interfaces. |

**Catch:** `public` is the least restrictive choice rather than a public-only mode; `protected` also permits private interfaces.

### `ip telnet session max-count` — changes settings

Limits the number of simultaneous Telnet sessions.

**RCI** `/rci/ip/telnet/session/max-count`

**Arguments:**

| Argument | Notes |
|---|---|
| `count` | Maximum simultaneous sessions, from 1 through 4. |

**Catch:** `no session max-count` resets the limit to the documented default of 4 sessions.

### `ip telnet session timeout` — changes settings

Sets how long an inactive Telnet session may remain before the timeout is applied.

**RCI** `/rci/ip/telnet/session/timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Inactive-session lifetime in seconds, from 5 through 2^32−1. |

**Catch:** a timeout of 300 seconds, including the value restored by `no session timeout`, means activity tracking is disabled rather than imposing a five-minute disconnect.

### `ip traffic-shape host` — changes settings

Limits download and upload rates for a known host, optionally under a schedule.

**RCI** `/rci/ip/traffic-shape/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | MAC address of the known host. |
| `rate` | Download limit in Kbps, from 64 Kbps to 1 Gbps. Without `asymmetric`, the examples show this value applied to both directions. |
| `upstream-rate` | Upload limit in Kbps, from 64 Kbps to 1 Gbps; used with the `asymmetric` form. |
| `schedule` | Name of a previously created schedule controlling the limit. |

**Catch:** supplying `rate` alone makes download and upload equal, while `asymmetric` separates the upload limit; adding a schedule makes the limit conditional rather than continuously applied.

**Blast radius:** bare `no ip traffic-shape host` removes rate limits for every host.

### `ip traffic-shape unknown-host` — changes settings

Applies a bandwidth limit to unregistered devices, with an optional separate upload rate.

**RCI** `/rci/ip/traffic-shape/unknown-host/rate`

**Arguments:**

| Argument | Notes |
|---|---|
| `rate` | Download rate in Kbps, from 64 Kbps through 1 Gbps. |
| `upstream-rate` | Upload rate in Kbps, from 64 Kbps through 1 Gbps; used with the `asymmetric` form. |

**Catch:** the plain form limits both directions with the single `rate`; adding `asymmetric upstream-rate` makes the upload limit distinct from the download limit.
