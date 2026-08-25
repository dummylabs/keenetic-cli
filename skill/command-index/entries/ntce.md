# `ntce` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ntce` — read-only

Enters the command group for configuring the NTCE service.

**RCI** `/rci/ntce`

**Catch:** NONE

---

### `ntce filter assign host` — changes settings

Assigns an NTCE filter profile to a registered host.

**RCI** `/rci/ntce/filter/assign/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | MAC address of a registered host. |
| `profile` | NTCE filter profile name. |

**Catch:** the first example enters `04:12:c4:54:bc:59` but the confirmation names `04:d4:12:54:bc:59`, and the later removal uses the latter; this is an unexplained example inconsistency, not evidence that the input is normalized that way.

**Blast radius:** bare `no filter assign host` removes profiles from all hosts.

### `ntce filter assign interface` — changes settings

Assigns an NTCE filter profile to a network interface.

**RCI** `/rci/ntce/filter/assign/interface`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Network interface name. |
| `profile` | NTCE filter profile name. |

**Catch:** NONE

**Blast radius:** bare `no filter assign interface` removes profiles from every interface.
