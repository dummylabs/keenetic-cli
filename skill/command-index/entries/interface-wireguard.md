# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface wireguard asc` — changes settings

Configures WireGuard Advanced Security Configuration parameters.

**RCI** `/rci/interface/wireguard/asc`

**Arguments:**

| Argument | Notes |
|---|---|
| `jc` | Number of random-data packets sent before session start. |
| `jmin` | Minimum size of a junk packet. |
| `jmax` | Maximum size of a junk packet. |
| `s1` | Random-data size added to the initiation packet. |
| `s2` | Random-data size added to the response packet. |
| `h1` | First-byte header for the handshake. |
| `h2` | First-byte header for the handshake response. |
| `h3` | Header used for an UnderLoad packet. |
| `h4` | Header used for a data packet. |

**Catch:** NONE

### `interface wireguard listen-port` — changes settings

Assigns the UDP port that accepts incoming WireGuard connections.

**RCI** `/rci/interface/wireguard/listen-port`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | UDP port from 1 through 65535. |

**Catch:** NONE

### `interface wireguard obfs-key` — changes settings

Configures an obfuscation key compatible with DD-WRT.

**RCI** `/rci/interface/wireguard/obfs-key`

**Arguments:**

| Argument | Notes |
|---|---|
| `obfs-key` | Key of 1–32 characters using the documented Latin letters, digits, dots, hyphens, and underscores. |

**Catch:** the example supplies punctuation outside the documented character set and still reports success, while the success message identifies a peer rather than echoing the configured obfuscation key; the block does not explain either discrepancy.

### `interface wireguard peer` — changes settings

Registers a remote peer by its public key and enters that peer's configuration context.

**RCI** `/rci/interface/wireguard/peer`

**Arguments:**

| Argument | Notes |
|---|---|
| `key` | 44-character Base64 representation of a 32-byte public key, using letters, digits, and equals signs. |

**Catch:** the example's removal message does not reproduce the same key suffix as the key entered, so a caller should not blindly use the echoed removal text as the peer identifier without checking it.

### `interface wireguard peer allow-ips` — changes settings

Adds one permitted subnet to a WireGuard peer's tunnel.

**RCI** `/rci/interface/wireguard/peer/allow-ips`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` + `mask` | The permitted subnet. `0.0.0.0/0` permits every destination, which is how a full-tunnel peer is configured. |

**Catch:** each call **adds** a subnet rather than replacing the set, so configuring a peer means removing what you do not want as well as adding what you do.

**Blast radius:** `no ... allow-ips <address> <mask>` removes that one subnet, but the bare `no ... allow-ips` with no argument removes **every** subnet on the peer — which drops the peer's routing entirely rather than trimming it.

### `interface wireguard peer client-id send` — changes settings

Sets the client ID sent in WireGuard message headers for the selected peer.

**RCI** `/rci/interface/wireguard/peer/client-id/send`

**Arguments:**

| Argument | Notes |
|---|---|
| `client-id` | Decimal form of the translated identifier, from 1 through 16777215. |

**Catch:** NONE

### `interface wireguard peer connect` — changes settings

Constrains a WireGuard peer connection to a chosen interface.

**RCI** `/rci/interface/wireguard/peer/connect`

**Arguments:**

| Argument | Notes |
|---|---|
| `via` | Full interface name or alias through which the peer connects. |

**Catch:** although the description says the bare `no connect` restores the default connection choice, the example reports that it disables the peer; the block does not resolve that difference.

### `interface wireguard peer endpoint` — changes settings

Assigns the remote address and optional UDP port for a WireGuard peer.

**RCI** `/rci/interface/wireguard/peer/endpoint`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Server IP address or domain name. |
| `port` | UDP server port when supplied. |

**Catch:** NONE

### `interface wireguard peer keepalive-interval` — changes settings

Sets periodic keepalive timing for monitoring a WireGuard peer connection.

**RCI** `/rci/interface/wireguard/peer/keepalive-interval`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | Keepalive period from 3 through 3600 seconds. |

**Catch:** NONE

### `interface wireguard peer obfs-key` — changes settings

Configures an obfuscation key for the selected WireGuard peer.

**RCI** `/rci/interface/wireguard/peer/obfs-key`

**Arguments:**

| Argument | Notes |
|---|---|
| `obfs-key` | Key of 1–32 characters using the documented Latin letters, digits, dots, hyphens, and underscores. |

**Catch:** the example uses punctuation outside the documented character set yet reports the key as set, so the block does not establish that the stated alphabet is enforced.

### `interface wireguard peer preshared-key` — changes settings

Stores the optional pre-shared key for a WireGuard peer.

**RCI** `/rci/interface/wireguard/peer/preshared-key`

**Arguments:**

| Argument | Notes |
|---|---|
| `preshared-key` | 44-character key made from Latin letters, digits, and equals signs. |

**Catch:** the command transcript contains the supplied PSK in clear text, so recording terminal input or command logs exposes a peer secret.

### `interface wireguard private-key` — read-only

Sets a WireGuard private key or asks the interface to generate one.

**RCI** `/rci/interface/wireguard/private-key`

**Arguments:**

| Argument | Notes |
|---|---|
| `private-key` | A 44-character key using Latin letters, digits, and `=`; omitting it selects key generation. |

**Catch:** Omitting the key generates a new identity, and the example shows an explicitly supplied private key echoed in the CLI output, so command output must be treated as secret-bearing.
