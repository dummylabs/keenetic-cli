# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface ip access-group` — changes settings

Associates named ACLs with an interface for inbound or outbound traffic.

**RCI** `/rci/interface/ip/access-group`

**Catch:** the same ACL can be assigned independently to each traffic direction, while the `no` form can target a particular assignment or omit the ACL and direction entirely.


**Arguments:**

| Argument | Notes |
|---|---|
| `acl` | The name of an ACL previously created with `access-list`. |
| `direction` | `in` applies to incoming packets; `out` applies to outgoing packets. |

### `interface ip address` — changes settings

Sets the network interface's IP address and mask.

**RCI** `/rci/interface/ip/address`

**Catch:** the example supplies `address/prefix` as one token even though the synopsis lists separate address and mask arguments; a running automatic address-configuration service, such as the DHCP client, can also overwrite the manual address.

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | The interface IP address. |
| `mask` | The mask may use canonical notation or a prefix length such as `/24`. |

### `interface ip address dhcp` — changes settings

Starts or stops DHCP-based configuration of the interface's address, DNS servers, and default gateway.

**RCI** `/rci/interface/ip/address/dhcp`

**Catch:** stopping the client removes dynamically supplied settings; the documented restoration guarantee specifically covers the previous IP address and mask, not a prior value for DNS or the default gateway.

### `interface ip adjust-ttl recv` — changes settings

Sets the TTL adjustment applied to inbound packets on the interface.

**RCI** `/rci/interface/ip/adjust-ttl/recv`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `recv` | An integer from 1 through 255. |

### `interface ip adjust-ttl send` — changes settings

Sets the TTL adjustment applied to outbound packets on the interface.

**RCI** `/rci/interface/ip/adjust-ttl/send`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `send` | An integer from 1 through 255. |

### `interface ip alias` — changes settings

Assigns an additional IPv4 address to an interface as an alias.

**RCI** `/rci/interface/ip/alias`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Additional interface address. |
| `mask` | Accepts either a dotted mask or a prefix length such as `/24`. |

**Catch:** the targeted no-form resets the matching alias to the sentinel `0.0.0.0/0` rather than simply making an address disappear; the example shows the alias slot being reset.

**Blast radius:** bare `no ip alias` removes every alias from the interface.

### `interface ip dhcp client broadcast` — changes settings

Controls the broadcast bit in DHCP Discover messages.

**RCI** `/rci/interface/ip/dhcp/client/broadcast`

**Catch:** NONE

### `interface ip dhcp client class-id` — changes settings

Sets the DHCP vendor-class identifier sent by the client.

**RCI** `/rci/interface/ip/dhcp/client/class-id`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `class` | The vendor class name, enclosed in double quotes. |

### `interface ip dhcp client debug` — changes settings

Enables or disables detailed DHCP-client diagnostics.

**RCI** `/rci/interface/ip/dhcp/client/debug`

**Catch:** diagnostic details are written to the system log rather than emitted as this command's result.

### `interface ip dhcp client displace` — changes settings

Configures displacement of a named interface's static address when it conflicts with the main interface's DHCP address.

**RCI** `/rci/interface/ip/dhcp/client/displace`

**Catch:** when automatically triggered by connecting a USB Ethernet adapter, the command saves configuration and restarts the router; `check-session` prevents that reboot and network-address change when active SCGI sessions exist.

**Arguments:**

| Argument | Notes |
|---|---|
| `what` | The name or alias of the interface whose static address is displaced. |
| `check-session` | Prevents rebooting and changing the router's network address when SCGI sessions are active; without it, the command is added to `default-config`. |

### `interface ip dhcp client dns-routes` — changes settings

Controls automatic host routes to DNS servers received from DHCP.

**RCI** `/rci/interface/ip/dhcp/client/dns-routes`

**Catch:** NONE

### `interface ip dhcp client fallback` — changes settings

Selects a static-address fallback for DHCP errors.

**RCI** `/rci/interface/ip/dhcp/client/fallback`

**Catch:** the `no` form cancels the fallback by setting its address to `0.0.0.0`, rather than restoring an earlier fallback address.

**Arguments:**

| Argument | Notes |
|---|---|
| `type` | The only implemented type is `static`. |

### `interface ip dhcp client hostname` — changes settings

Sets the host name sent in DHCP requests.

**RCI** `/rci/interface/ip/dhcp/client/hostname`

**Catch:** the `no` form restores the client hostname's default instead of clearing it to an empty value.

**Arguments:**

| Argument | Notes |
|---|---|
| `hostname` | The host name to assign. |

### `interface ip dhcp client name-servers` — changes settings

Controls whether the client uses DNS server addresses supplied by DHCP.

**RCI** `/rci/interface/ip/dhcp/client/name-servers`

**Catch:** NONE

### `interface ip dhcp client release` — changes settings

Releases the DHCP lease and places the client into a sleep state.

**RCI** `/rci/interface/ip/dhcp/client/release`

**Catch:** the command is stateful: after one invocation puts the client to sleep, executing it again returns the client to automatic address acquisition.

### `interface ip dhcp client renew` — changes settings

Releases the current DHCP lease and begins obtaining a replacement address.

**RCI** `/rci/interface/ip/dhcp/client/renew`

**Catch:** renewal is a release-then-acquire operation rather than merely extending the existing lease.

### `interface ip dhcp client routes` — changes settings

Controls acceptance of provider routes carried in DHCP options 33, 121, and 242.

**RCI** `/rci/interface/ip/dhcp/client/routes`

**Catch:** the feature is enabled by default, and the block says the configuration displays this command only in its no-prefix form.

### `interface ip flow` — changes settings

Enables NetFlow collection for incoming, outgoing, or both traffic directions.

**RCI** `/rci/interface/ip/flow`

**Catch:** the direction is selectable only on the positive command; `no ip flow` has no direction argument and disables the sensor as a whole.

**Arguments:**

| Argument | Notes |
|---|---|
| `direction` | `ingress` collects incoming traffic, `egress` outgoing traffic, and `both` both directions. |

### `interface ip global` — changes settings

Assigns the interface a global-network priority or an automatically calculated ordering.

**RCI** `/rci/interface/ip/global`

**Catch:** the example maps input `order 0` to a reported order of 1; treat the argument as a placement position rather than assuming the submitted number is echoed back, although the block does not define the general indexing rule.

**Arguments:**

| Argument | Notes |
|---|---|
| `priority` | An integer from 1 through 65534 used for default-route priority. |
| `order` | A relative interface position from 0 through 65534, limited by the number of global interfaces. |
| `auto` | Requests automatic priority calculation. |

### `interface ip mru` — changes settings

Sets the MRU advertised to a remote PPP peer during IPCP connection setup.

**RCI** `/rci/interface/ip/mru`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `mru` | The MRU value to save. |

### `interface ip mtu` — changes settings

Sets a static MTU for the network interface.

**RCI** `/rci/interface/ip/mtu`

**Catch:** the `no` form restores the MTU from before the command was first used, so it is not necessarily a universal factory value; on PPP connections the configured MTU is sent even when the peer requested a lower one.

**Arguments:**

| Argument | Notes |
|---|---|
| `mtu` | An integer from 64 through 65535. |

### `interface ip name-servers` — changes settings

Controls whether the interface accepts DNS server addresses.

**RCI** `/rci/interface/ip/name-servers`

**Catch:** NONE

### `interface ip nat loopback` — changes settings

Controls reverse NAT for reaching a local server through its Internet-facing address.

**RCI** `/rci/interface/ip/nat/loopback`

**Catch:** loopback is enabled by default on Home interfaces at private and protected security levels, so the `no` form explicitly disables a behavior that is otherwise already active there.

### `interface ip remote` — changes settings

Sets a static address for the remote PPP peer.

**RCI** `/rci/interface/ip/remote`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | The remote peer IP address. |

### `interface ip tcp adjust-mss` — changes settings

Limits the MSS advertised in outgoing TCP SYN packets on the interface.

**RCI** `/rci/interface/ip/tcp/adjust-mss`

**Catch:** the setting applies to every outgoing TCP SYN on the interface, and the `no` form removes all MSS limits rather than reverting one selected limit.

**Arguments:**

| Argument | Notes |
|---|---|
| `pmtu` | Uses the path's minimum MTU as the MSS ceiling. |
| `mss` | The explicit integer MSS ceiling. |
