# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip dhcp class` — read-only

Selects a DHCP vendor class, creating it when the named class is absent.

**RCI** `/rci/ip/dhcp/class`

**Arguments:**

| Argument | Notes |
|---|---|
| `class` | Vendor-class name; an unknown name is created by the command. |

**Catch:** A lookup miss is treated as a create request, so a typo in the class name can add a new class instead of failing.

### `ip dhcp class option` — changes settings

Sets the hexadecimal vendor-class matching option for a DHCP class.

**RCI** `/rci/ip/dhcp/class/option`

**Arguments:**

| Argument | Notes |
|---|---|
| `number` | The block documents only option number `60`. |
| `data` | Hexadecimal option value. |

**Catch:** NONE

### `ip dhcp host` — changes settings

Creates or updates a static DHCP host binding between an address and a MAC address.

**RCI** `/rci/ip/dhcp/host`

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | Arbitrary name used to identify the binding. |
| `mac` | MAC address; when omitted, the prior configured value is retained. |
| `ip` | IP address; when omitted, the prior configured value is retained. |

**Catch:** an address outside every configured pool remains stored but has no effect on DHCP service; the command can also update only the MAC or only the IP while preserving the other value.

### `ip dhcp pool` — changes settings

Creates or selects a DHCP pool and enters its pool-specific configuration context.

**RCI** `/rci/ip/dhcp/pool`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Pool name, up to 32 characters; at most 32 pools can be entered. |

**Catch:** configuring a pool alone does not start DHCP service—the separate DHCP service must be enabled—and the block says only one pool per interface is supported; its address range must belong to a network on an Ethernet interface for the server to function correctly.

### `ip dhcp pool bind` — changes settings

Associates the current DHCP pool with an interface.

**RCI** `/rci/ip/dhcp/pool/bind`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full Ethernet-interface name or alias. |

**Catch:** NONE

### `ip dhcp pool bootfile` — changes settings

Sets the DHCP option 67 boot-file path.

**RCI** `/rci/ip/dhcp/pool/bootfile`

**Arguments:**

| Argument | Notes |
|---|---|
| `bootfile` | Boot-file path. |

**Catch:** NONE

### `ip dhcp pool class` — changes settings

Creates or selects a vendor class within the current DHCP pool.

**RCI** `/rci/ip/dhcp/pool/class`

**Arguments:**

| Argument | Notes |
|---|---|
| `class` | Vendor-class name. |

**Catch:** the class name must match the name used by the separate `ip dhcp class` command for matching to work; an unknown name is created rather than rejected.

### `ip dhcp pool class option` — changes settings

Adds a vendor-class-specific DHCP option to the current pool class.

**RCI** `/rci/ip/dhcp/pool/class/option`

**Arguments:**

| Argument | Notes |
|---|---|
| `number` | Option `6` is DNS, `42` is NTP, and `43` is vendor-specific information. |
| `type` | `ip` is available for the DNS and NTP options but not for option `43`; `hex` selects hexadecimal data. |
| `data` | Option value in the selected representation. |

**Catch:** NONE

### `ip dhcp pool debug` — changes settings

Controls emission of DHCP-pool debugging messages into the system log.

**RCI** `/rci/ip/dhcp/pool/debug`

**Catch:** NONE

### `ip dhcp pool default-router` — changes settings

Sets the default gateway advertised by the DHCP pool.

**RCI** `/rci/ip/dhcp/pool/default-router`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Gateway IP address. |

**Catch:** without an explicit gateway, the router derives one from the Ethernet interface selected for the pool's range rather than leaving the gateway unset.

### `ip dhcp pool dns-server` — changes settings

Sets the DNS servers advertised through DHCP option 6.

**RCI** `/rci/ip/dhcp/pool/dns-server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address1` | Primary DNS server address. |
| `address2` | Optional secondary DNS server address. |
| `disable` | Disables DHCP option 6. |

**Catch:** `disable` is an alternative to supplying addresses and suppresses the DNS-server option entirely; if no addresses are configured, the selected range's Ethernet interface supplies the default server address.

### `ip dhcp pool domain` — changes settings

Sets the local domain advertised to DHCP clients for DNS resolution.

**RCI** `/rci/ip/dhcp/pool/domain`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | Local domain name. |

**Catch:** NONE

### `ip dhcp pool enable` — changes settings

Activates the current DHCP pool for system use.

**RCI** `/rci/ip/dhcp/pool/enable`

**Catch:** NONE

### `ip dhcp pool lease` — changes settings

Sets the DHCP address lease duration for the current pool.

**RCI** `/rci/ip/dhcp/pool/lease`

**Arguments:**

| Argument | Notes |
|---|---|
| `lease` | Duration from 1 through 259200 seconds. |

**Catch:** the bare `no lease` form restores the documented default of 25200 seconds rather than removing the lease-time setting without a replacement.

### `ip dhcp pool next-server` — changes settings

Sets the DHCP option 66 TFTP server address.

**RCI** `/rci/ip/dhcp/pool/next-server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | TFTP server IP address. |

**Catch:** NONE

### `ip dhcp pool option` — changes settings

Adds an additional DHCP-server option to the current pool.

**RCI** `/rci/ip/dhcp/pool/option`

**Arguments:**

| Argument | Notes |
|---|---|
| `number` | Documented options include `4`, `6`, `42`, `44`, `26`, `121`, and `249`; options `121` and `249` encode classless routes. |
| `type` | `hex` selects hexadecimal data, `ascii` selects ASCII data, and `ip` selects IP-address data; `ip` is unavailable for option `26`, and the block says it is not specified as a command keyword. |
| `data` | Option value in the selected representation. |

**Catch:** the examples successfully set options `60` and `150`, although neither appears in the documented option-number list; the block therefore does not establish the complete accepted-number set, and the example's explicit `ip` token for option `150` also conflicts with the note that `ip` is not specified as a command keyword.

### `ip dhcp pool range` — changes settings

Defines the dynamic address range issued by the current DHCP pool.

**RCI** `/rci/ip/dhcp/pool/range`

**Arguments:**

| Argument | Notes |
|---|---|
| `begin` | Starting pool address. |
| `end` | Ending pool address when using an explicit endpoint. |
| `size` | Pool size when using a starting address and count. |

**Catch:** the router chooses the Ethernet interface for the range automatically, and that choice also supplies the default gateway and DNS server unless those values are set separately.

### `ip dhcp pool update-dns` — changes settings

Controls adding DHCP-assigned hostnames as static records in the DNS proxy.

**RCI** `/rci/ip/dhcp/pool/update-dns`

**Catch:** NONE

### `ip dhcp pool wpad` — changes settings

Configures DHCP option 252 with a proxy URL for WPAD.

**RCI** `/rci/ip/dhcp/pool/wpad`

**Arguments:**

| Argument | Notes |
|---|---|
| `wpad` | URL of the proxy configuration resource. |

**Catch:** NONE

### `ip dhcp relay enable` — changes settings

Enables DHCP relay on an interface.

**RCI** `/rci/ip/dhcp/relay/enable`

**Catch:** enabling relay takes precedence over the router's own DHCP server on that interface.

### `ip dhcp relay lan` — changes settings

Adds a LAN interface to the set on which the DHCP relay accepts client requests.

**RCI** `/rci/ip/dhcp/relay/lan`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full Ethernet interface name or alias. |

**Catch:** the block requires one command per desired LAN interface, so repeated calls build the set instead of replacing it with a single multi-interface value.

**Blast radius:** bare `no ip dhcp relay lan` disables the relay on every interface.

### `ip dhcp relay server` — changes settings

Sets the DHCP server to which relay requests from the LAN are forwarded.

**RCI** `/rci/ip/dhcp/relay/server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | IP address of the DHCP server receiving the relayed requests. |

**Catch:** NONE

### `ip dhcp relay upstream interface` — changes settings

Binds DHCP relay's upstream traffic to a selected interface.

**RCI** `/rci/ip/dhcp/relay/upstream/interface`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full interface name or an alias. |

**Catch:** NONE

### `ip dhcp relay upstream server` — changes settings

Sets the DHCP server address used for upstream relay forwarding.

**RCI** `/rci/ip/dhcp/relay/upstream/server`

**Arguments:**

| Argument | Notes |
|---|---|
| `server` | IP address of the upstream DHCP server. |

**Catch:** NONE

### `ip dhcp relay wan` — changes settings

Selects the WAN-side interface through which DHCP relay reaches the higher-level server.

**RCI** `/rci/ip/dhcp/relay/wan`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full name or alias of the Ethernet interface used to send client requests. |

**Catch:** the system permits only one interface of this WAN relay type; without a configured server address, requests are broadcast rather than sent to a specific server.
