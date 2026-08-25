# `upnp` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `upnp forward` — changes settings

Adds a UPnP port-forwarding rule.

**RCI** `/rci/upnp/forward`

**Arguments:**

| Argument | Notes |
|---|---|
| `protocol` | Either `tcp` or `udp`. |
| `interface` | Interface name used when adding a rule; the block documents it only for addition. |
| `address` | IP address used in the forwarding rule. |
| `port` | Port used in the forwarding rule. |
| `index` | List position used to remove a rule. |

**Catch:** removal is not symmetric with addition: it can select an index or the protocol/address/port tuple, while the documented interface selector is add-only.

---

### `upnp lan` — changes settings

Selects the LAN interface on which UPnP runs.

**RCI** `/rci/upnp/lan`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Accepts a full interface name or an alias. |

**Catch:** UPnP can serve only one network segment, so this setting cannot represent multiple LAN segments at once.

---

### `upnp redirect` — changes settings

Adds or removes a UPnP port-translation rule.

**RCI** `/rci/upnp/redirect`

**Arguments:**

| Argument | Notes |
|---|---|
| `protocol` | `tcp` or `udp`. |
| `interface` | Interface for the rule. |
| `port` | The incoming port the rule matches. |
| `to-address` | Destination IP address. |
| `to-port` | Optional port on the target host. The block does not say what happens when it is omitted, so pass it explicitly. |
| `and forward` | Special removal keyword that selects both forwarding and redirecting lists. |
| `index` | Number of the rule in the list to remove. |

**Catch:** the no-form's `(protocol port)` selector omits interface and destination details, so it cannot distinguish rules sharing that pair; use the list index when the pair is not unique.

**Blast radius:** bare `no upnp redirect` removes every redirect rule, while `no upnp redirect and forward` clears both forwarding and redirecting rule lists.
