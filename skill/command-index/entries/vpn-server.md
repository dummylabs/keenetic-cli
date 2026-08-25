# `vpn-server` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `vpn-server` — read-only

Provides the CLI context for VPN-server configuration commands.

**RCI** `/rci/vpn-server`

**Catch:** NONE

### `vpn-server dhcp route` — changes settings

Adds a route delivered in DHCP INFORM messages to VPN server clients.

**RCI** `/rci/vpn-server/dhcp/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Network address for the client route. |
| `mask` | May be entered as a dotted mask or a prefix length such as `/24`. |

**Catch:** NONE

**Blast radius:** bare `no dhcp route` clears every DHCP INFORM route for the VPN server.
