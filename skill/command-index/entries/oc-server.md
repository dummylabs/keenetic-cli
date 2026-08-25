# `oc-server` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `oc-server` — read-only

Enters the command group for configuring OpenConnect server parameters.

**RCI** `/rci/oc-server`

**Catch:** NONE

---

### `oc-server route` — changes settings

Adds a route delivered in DHCP INFORM messages to OpenConnect server clients.

**RCI** `/rci/oc-server/route`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Network address for the client route. |
| `mask` | May be entered as a dotted mask or a prefix length such as `/24`. |

**Catch:** NONE

**Blast radius:** bare `no route` clears every DHCP INFORM route for the OpenConnect server.
