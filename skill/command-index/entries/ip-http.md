# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip http lockout-policy` — changes settings

Configures HTTP brute-force detection thresholds and timing for public interfaces.

**RCI** `/rci/ip/http/lockout-policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | Failed-login count; default 5, permitted range 4–20, or `0` for the reset operation. |
| `duration` | Authorization-ban duration in minutes; default 15, range 1–60. |
| `observation-window` | Suspicious-activity observation period in minutes; default 3, range 1–10. |

**Catch:** `0` is a sentinel on the threshold argument: it resets all brute-force detection parameters to their defaults rather than configuring a zero-attempt threshold.

### `ip http log access` — changes settings

Controls access diagnostics for the router's nginx web server.

**RCI** `/rci/ip/http/log/access`

**Catch:** the command is described as enabling web-server debug mode, while the example labels the resulting log as access logging; do not treat it as a general-purpose HTTP logging switch.

### `ip http log auth` — changes settings

Records unsuccessful authorization attempts for the web service.

**RCI** `/rci/ip/http/log/auth`

**Catch:** only failed authorization attempts are in scope; the block does not say that successful logins or other web requests are recorded.

### `ip http log webdav` — changes settings

Records failed connection activity for the WebDAV server.

**RCI** `/rci/ip/http/log/webdav`

**Catch:** the description limits this to failed connection attempts, whereas the example calls the output request tracing, so it does not establish that successful WebDAV traffic is logged.

### `ip http port` — changes settings

Sets the port used by the router's HTTP web interface, defaulting to 80.

**RCI** `/rci/ip/http/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | Integer port number for the HTTP interface. |

**Catch:** NONE

### `ip http proxy` — changes settings

Enters the configuration context for a named HTTP proxy, creating it when necessary.

**RCI** `/rci/ip/http/proxy`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Name assigned to the HTTP proxy. |

**Catch:** a positive invocation is create-or-select: a missing named proxy is created instead of being rejected.

### `ip http proxy auth` — changes settings

Enables password authorization for the current HTTP proxy.

**RCI** `/rci/ip/http/proxy/auth`

**Catch:** NONE

### `ip http proxy dns-override` — changes settings

Controls the local DNS override used for fourth-level KeenDNS names.

**RCI** `/rci/ip/http/proxy/dns-override`

**Catch:** disabling the feature also removes the documented static DNS A-record used for local access to the fourth-level KeenDNS name; it is not just a logging or lookup preference toggle.

### `ip http proxy domain` — changes settings

Assigns a static domain name as the virtual host's FQDN.

**RCI** `/rci/ip/http/proxy/domain`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Domain name used for the proxy virtual host. |

**Catch:** the example's bare `no domain` reports removal of an NDNS domain even though the positive form configures a static domain, so the example does not establish that this reset targets only the static value.

### `ip http proxy domain ndns` — changes settings

Selects NDNS as the source of the HTTP proxy domain.

**RCI** `/rci/ip/http/proxy/domain/ndns`

**Catch:** enabling NDNS domain mode deletes the separately configured static proxy domain, so the two domain-selection methods are not retained together.

### `ip http proxy force-host` — changes settings

Sets the upstream Host header value to a supplied address or name.

**RCI** `/rci/ip/http/proxy/force-host`

**Arguments:**

| Argument | Notes |
|---|---|
| `force-host` | IP address or domain name to enforce in the upstream Host header. |

**Catch:** NONE

### `ip http proxy preserve-host` — changes settings

Controls preservation of the original Host header while proxying.

**RCI** `/rci/ip/http/proxy/preserve-host`

**Catch:** NONE

### `ip http proxy preserve-origin` — changes settings

Controls preservation of the Origin header while proxying.

**RCI** `/rci/ip/http/proxy/preserve-origin`

**Catch:** NONE

### `ip http proxy preserve-referer` — changes settings

Controls preservation of the Referer header while proxying.

**RCI** `/rci/ip/http/proxy/preserve-referer`

**Catch:** NONE

### `ip http proxy security-level` — changes settings

Sets which interface classes may reach the HTTP proxy, with private as the default.

**RCI** `/rci/ip/http/proxy/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Permits proxy access from public, private, and protected interfaces. |
| `private` | Permits proxy access from private interfaces only. |

**Catch:** the bare `no security-level` form restores the default private level rather than disabling the proxy service.

### `ip http proxy ssl redirect` — changes settings

Controls automatic HTTP-to-SSL redirection for proxy domains that have an SSL certificate.

**RCI** `/rci/ip/http/proxy/ssl/redirect`

**Catch:** the example uses the global-looking `ip http ssl redirect` spelling even though this block is scoped to the proxy context; treat that mismatch as a documentation inconsistency rather than proof that the global command configures this proxy.

### `ip http proxy timeout` — changes settings

Sets the HTTP proxy's upstream connection timeout, defaulting to 60 seconds.

**RCI** `/rci/ip/http/proxy/timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Timeout in seconds, from 5 through 86400. |

**Catch:** NONE

### `ip http proxy upstream` — changes settings

Selects the protocol and endpoint used as the HTTP proxy's upstream destination.

**RCI** `/rci/ip/http/proxy/upstream`

**Arguments:**

| Argument | Notes |
|---|---|
| `http` | Keyword selecting an HTTP upstream. |
| `https` | Keyword selecting an HTTPS upstream. |
| `connect` | Keyword selecting the OpenVPN-server address-and-port mode. |
| `mac` | MAC address of the upstream server. |
| `ip` | IP address of the upstream server. |
| `fqdn` | Fully qualified domain name of the upstream server. |
| `port` | Port number of the upstream server. |

**Catch:** the `connect` protocol keyword is documented for an OpenVPN server, so it is not interchangeable with the HTTP and HTTPS upstream modes.

### `ip http proxy x-real-ip` — changes settings

Controls forwarding support for X-Real-IP and X-Forwarded-For headers.

**RCI** `/rci/ip/http/proxy/x-real-ip`

**Catch:** the two headers are enabled and disabled as one combined option; the block provides no separate control for either header.

### `ip http security-level` — changes settings

Sets the interface exposure and transport allowed for the Keenetic web interface.

**RCI** `/rci/ip/http/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Allows web-interface access from public, private, and protected interfaces over HTTP and HTTPS. |
| `private` | Allows access from private interfaces. |
| `protected` | Allows access from private and protected interfaces. |
| `ssl` | Modifier that restricts public-interface access to HTTPS. |

**Catch:** `ssl` is an optional modifier of `public`, not an independent security level; the synopsis does not permit it with `private` or `protected`.

### `ip http ssl acme debug` — changes settings

Turns on debug output for the ACME service, off by default.

**RCI** `/rci/ip/http/ssl/acme/debug`

**Catch:** NONE

### `ip http ssl acme ecdsa` — changes settings

Controls support for ECDSA-based certificates in the ACME service.

**RCI** `/rci/ip/http/ssl/acme/ecdsa`

**Catch:** NONE

### `ip http ssl acme get` — read-only

Begins certificate generation and signing for a domain through ACME.

**RCI** `/rci/ip/http/ssl/acme/get`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Domain for which the certificate is requested; the documented default is the KeenDNS domain. |

**Catch:** The example reports that certificate acquisition has started, so completion is not synchronous; the domain must also be reachable from the Internet for the documented process to work.

### `ip http ssl acme list` — read-only

Lists the system's free Let's Encrypt certificates.

**RCI** `/rci/ip/http/ssl/acme/list`

**Catch:** Certificates appear as repeated `certificate` records, so the response should be parsed as a collection rather than as one certificate object.

**Returns (fields):** `certificate`, `domain`, `should-be-renewed`, `is-expired`, `issue-time`, `expiration-time`.

### `ip http ssl acme revoke` — read-only

Begins revocation and removal of a certificate for a domain.

**RCI** `/rci/ip/http/ssl/acme/revoke`

**Arguments:**

| Argument | Notes |
|---|---|
| `revoke` | KeenDNS domain whose certificate is to be revoked. |

**Catch:** The example says revocation has started rather than completed, so callers must not treat the command's immediate acknowledgement as proof that the certificate is already gone.

### `ip http ssl enable` — changes settings

Controls the router's HTTPS server.

**RCI** `/rci/ip/http/ssl/enable`

**Catch:** NONE

### `ip http ssl port` — changes settings

Sets the port used by the router's HTTPS web interface, defaulting to 443.

**RCI** `/rci/ip/http/ssl/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | Integer port number for the HTTPS interface. |

**Catch:** NONE

### `ip http ssl redirect` — changes settings

Controls automatic redirection to SSL for domains with an SSL certificate.

**RCI** `/rci/ip/http/ssl/redirect`

**Catch:** the redirect is conditional on the domain having an SSL certificate; this is not documented as a blanket redirect for every HTTP domain.

### `ip http webdav` — read-only

Enters the command group for managing the WebDAV server.

**RCI** `/rci/ip/http/webdav`

**Catch:** NONE

### `ip http webdav enable` — changes settings

Controls whether the WebDAV server is active.

**RCI** `/rci/ip/http/webdav/enable`

**Catch:** NONE

### `ip http webdav permissive` — changes settings

Controls unauthenticated access to the WebDAV server.

**RCI** `/rci/ip/http/webdav/permissive`

**Catch:** enabling permissive mode grants every user WebDAV access without authentication.

### `ip http webdav security-level` — changes settings

Sets which interface classes may reach the WebDAV server, with private as the default.

**RCI** `/rci/ip/http/webdav/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Permits WebDAV access from public, private, and protected interfaces. |
| `private` | Permits WebDAV access from private interfaces only. |

**Catch:** the levels are not an unrestricted-to-restricted toggle: `public` includes all three interface classes, while `private` excludes both public and protected interfaces.

### `ip http x-frame-options` — changes settings

Sets the X-Frame-Options response header for the web server in the Home segment.

**RCI** `/rci/ip/http/x-frame-options`

**Arguments:**

| Argument | Notes |
|---|---|
| `x-frame-options` | Value to place in the X-Frame-Options header. |

**Catch:** the documented `no` syntax still includes the header-value argument, and the example repeats `DENY`; do not assume that a bare `no ip http x-frame-options` is accepted.
