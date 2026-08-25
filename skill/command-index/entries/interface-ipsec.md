# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface ipsec aggressive` — changes settings

Enables aggressive IKEv1 mode for compatibility with a FritzBox L2TP/IPsec server.

**RCI** `/rci/interface/ipsec/aggressive`

**Catch:** NONE

### `interface ipsec encryption-level` — changes settings

Selects the algorithm and PFS profile used by the automatically associated IPSec connection.

**RCI** `/rci/interface/ipsec/encryption-level`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `level` | One of the documented profiles: `weak`, `normal`, `normal-3des`, `strong`, `weak-pfs`, `normal-pfs`, `normal-3des-pfs`, `high`, `strong-aead`, or `strong-aead-pfs`. |

### `interface ipsec force-encaps` — changes settings

Forces ESP traffic for client tunnels into UDP encapsulation.

**RCI** `/rci/interface/ipsec/force-encaps`

**Catch:** NONE

### `interface ipsec ignore` — changes settings

Stops the IPSec service from processing incoming IKE packets on the selected interface.

**RCI** `/rci/interface/ipsec/ignore`

**Catch:** NONE

### `interface ipsec ikev2` — changes settings

Chooses IKEv2 instead of the default IKEv1 for the automatically associated IPSec connection.

**RCI** `/rci/interface/ipsec/ikev2`

**Catch:** the `no` form is a protocol selection, not merely a feature-off state: it restores IKEv1.

### `interface ipsec nail-up` — changes settings

Controls automatic secret-key changes for the listed IPsec tunnel types.

**RCI** `/rci/interface/ipsec/nail-up`

**Catch:** NONE

### `interface ipsec name-servers` — changes settings

Controls whether DNS addresses delivered by an IKEv1 or IKEv2 IPSec server are used.

**RCI** `/rci/interface/ipsec/name-servers`

**Catch:** NONE

### `interface ipsec preshared-key` — changes settings

Assigns the PSK for the automatically associated IPSec connection.

**RCI** `/rci/interface/ipsec/preshared-key`

**Catch:** setting the key also turns IPSec on for the tunnel; the example additionally contains a period even though the argument description lists only letters, digits, and `=` as accepted characters, so that stated restriction and the example should not be treated as consistent without verification.

**Arguments:**

| Argument | Notes |
|---|---|
| `key` | A 3–72 character secret; the block says letters, digits, and equal signs are accepted. |

### `interface ipsec proposal lifetime` — changes settings

Sets the Phase 1 IPSec transformation lifetime in seconds.

**RCI** `/rci/interface/ipsec/proposal/lifetime`

**Catch:** resetting the setting returns it to the fixed documented default of 28800 seconds rather than preserving a previously customized lifetime.

**Arguments:**

| Argument | Notes |
|---|---|
| `lifetime` | An integer from 60 through 2147483647 seconds. |

### `interface ipsec proposal local-id` — changes settings

Assigns a custom local IKE identifier.

**RCI** `/rci/interface/ipsec/proposal/local-id`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `local-id` | An IP address or domain name identifying the local host. |

### `interface ipsec proposal remote-id` — changes settings

Assigns a custom remote IKE identifier.

**RCI** `/rci/interface/ipsec/proposal/remote-id`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `remote-id` | An IP address or domain name identifying the remote host. |

### `interface ipsec transform-set lifetime` — changes settings

Sets the Phase 2 IPSec transformation lifetime in seconds.

**RCI** `/rci/interface/ipsec/transform-set/lifetime`

**Catch:** resetting the setting returns it to the fixed documented default of 28800 seconds rather than preserving a previously customized lifetime.

**Arguments:**

| Argument | Notes |
|---|---|
| `lifetime` | An integer from 60 through 2147483647 seconds. |
