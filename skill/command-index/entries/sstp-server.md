# `sstp-server` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `sstp-server` — read-only

Enters the command group for configuring SSTP server parameters.

**RCI** `/rci/sstp-server`

**Catch:** NONE

---

### `sstp-server dhcp route` — changes settings

Adds a route delivered in DHCP INFORM messages to SSTP server clients.

**RCI** `/rci/sstp-server/dhcp/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Network address for the client route. |
| `mask` | May be entered as a dotted mask or a prefix length such as `/24`; the example's prefix form is rendered as a dotted mask in the confirmation. |

**Catch:** NONE

**Blast radius:** bare `no dhcp route` clears every DHCP INFORM route for the SSTP server.
