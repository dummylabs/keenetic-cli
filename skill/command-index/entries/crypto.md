# `crypto` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `crypto ike proposal aead` — read-only

Enables AEAD cipher mode on the current IKE proposal.

**RCI** `/rci/crypto/ike/proposal/aead`

**Catch:** NONE

### `crypto ipsec transform-set aead` — read-only

Enables AEAD mode for an IPsec transform.

**RCI** `/rci/crypto/ipsec/transform-set/aead`

**Catch:** NONE

### `crypto map l2tp-server dhcp route` — changes settings

Adds a network route to the DHCP INFORM data sent to L2TP server clients.

**RCI** `/rci/crypto/map/l2tp-server/dhcp/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Network address for the client route. |
| `mask` | May be entered as a dotted mask or as a prefix length such as `/24`; the example supplies the address and prefix in one token. |

**Catch:** the route list accepts repeated entries, while the example's removal form without route arguments clears the list rather than targeting one route.

**Blast radius:** bare `no l2tp-server dhcp route` clears every DHCP INFORM route for the L2TP server.

### `crypto map virtual-ip dhcp route` — changes settings

Adds a network route to the DHCP INFORM data sent to Virtual IP server clients.

**RCI** `/rci/crypto/map/virtual-ip/dhcp/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Network address for the client route. |
| `mask` | Accepts either a dotted mask or a prefix length such as `/24`; the example combines the address and prefix in one token. |

**Catch:** the list has both a targeted removal form and a separate empty-argument form, so deleting one route and clearing all routes are distinct operations.

**Blast radius:** bare `no virtual-ip dhcp route` clears every DHCP INFORM route for the Virtual IP server.
