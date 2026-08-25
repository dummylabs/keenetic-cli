# `nextdns` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `nextdns` — read-only

Enters the command group for configuring NextDNS profiles.

**RCI** `/rci/nextdns`

**Catch:** NONE

---

### `nextdns assign` — changes settings

Associates a NextDNS protection profile with a host or network interface.

**RCI** `/rci/nextdns/assign`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Host MAC address. |
| `token` | NextDNS profile authentication token (ID). |
| `iface` | Full interface name or an alias. |

**Catch:** the positive interface form requires the literal `interface` keyword, while the synopsis and example disagree about the `no` form: the example removes an interface assignment with the token directly (`no assign Bridge0`). Do not assume the positive grammar is echoed by the removal command.

### `nextdns authenticate` — read-only

Supplies credentials for a NextDNS account.

**RCI** `/rci/nextdns/authenticate`

**Arguments:**

| Argument | Notes |
|---|---|
| `login` | The NextDNS account login. |
| `password` | The NextDNS account password; the example places it directly in the CLI command. |
| `pin` | An optional NextDNS account PIN. |

**Catch:** the block's synopsis shows `no authenticate` even though its Prefix no value is No, so the availability of that form should not be assumed without verification.

---

### `nextdns authtoken` — changes settings

Sets the authentication token for a NextDNS account.

**RCI** `/rci/nextdns/authtoken`

**Arguments:**

| Argument | Notes |
|---|---|
| `authtoken` | Authentication token ID for the NextDNS account. |

**Catch:** confirmations do not echo the token value, either when setting it or clearing it, so success output cannot be used to retrieve the credential.

### `nextdns check-availability` — read-only

Checks whether the NextDNS service is available.

**RCI** `/rci/nextdns/check-availability`

**Catch:** NONE

---
