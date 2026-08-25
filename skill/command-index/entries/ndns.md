# `ndns` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ndns` — read-only

Enters the command group for managing the Keenetic service.

**RCI** `/rci/ndns`

**Catch:** NONE

---

### `ndns book-name` — changes settings

Books a Public DNS hostname for a device.

**RCI** `/rci/ndns/book-name`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Hostname to allocate. |
| `domain` | Second-level domain for the hostname. |
| `access` | Access mode: `auto`, `cloud`, or `direct`; `cloud` tunnels HTTP traffic to the Hero and `direct` registers the Hero WAN address. |
| `access6` | `cloud` enables cloud mode for IPv6. |
| `transfer-code` | 32-symbol hexadecimal code used to transmit the booking to another Keenetic device; its lifetime is one week. |

**Catch:** transferring a booked hostname to another Keenetic is a two-sided operation: the same command with the same `transfer-code` must be run on both the sending and the receiving device, and the block gives the code a lifetime of one week.

**Returns (fields):** `name`, `domain`, `acme`, `updated`, `address`, `access`, `address6`, `access6`, `transfer`.

### `ndns check-name` — read-only

Checks whether a proposed hostname can be allocated.

**RCI** `/rci/ndns/check-name`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | The hostname to test for allocation. |

**Catch:** availability is reported per returned domain, not as one property of the name: the example has the same requested name available in one domain and unavailable in another.

**Returns (fields):** `list`, `item`, `domain`, `name`, `available`, `acme`.

---

### `ndns drop-name` — changes settings

Releases a previously booked Public DNS hostname.

**RCI** `/rci/ndns/drop-name`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Hostname to release. |
| `domain` | Second-level domain containing the hostname. |

**Catch:** NONE

### `ndns get-booked` — read-only

Fetches the server's current booking details for the public DNS hostname.

**RCI** `/rci/ndns/get-booked`

**Catch:** the example includes an `acme` value in the booking record even though `acme` is absent from the block's declared field list, so treat that key as an observation rather than a guaranteed field. The example also carries `0.0.0.0` and `::` as its address values; the block does not define whether those are sentinels.

**Returns (fields):** `name`, `domain`, `acme`, `updated`, `address`, `access`, `address6`, `access6`, `transfer`.

---

### `ndns get-update` — read-only

Updates the server-side allocation details for the device's public DNS hostname.

**RCI** `/rci/ndns/get-update`

**Arguments:**

| Argument | Notes |
|---|---|
| `access` | `auto` selects automatically; `cloud` registers against the cloud address and tunnels HTTP to the Hero; `direct` registers against the Hero WAN address and and, per the block, lets Static NAT (NAT 1-1) support be enabled. |
| `access6` | The only documented value is `cloud`, and it is supplied through the `ipv6` subcommand. |

**Catch:** the IPv6 mode is conditional: the `access6` argument is only used with `ipv6`, and the examples show `access6: none` when it is omitted but `access6: cloud` when it is explicitly supplied. The example records also include `acme`, although that key is not in the declared field list.

**Returns (fields):** `name`, `domain`, `acme`, `updated`, `address`, `access`, `address6`, `access6`, `transfer`.

---
