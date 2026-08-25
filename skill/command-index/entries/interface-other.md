# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface` — changes settings

Selects an interface context and can create a missing interface.

**RCI** `/rci/interface`

**Catch:** an unknown interface name triggers an attempted creation instead of simply failing a lookup; the `no` form removes the named interface.

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | May be a full interface name or an alias. |

### `interface atf disable` — changes settings

Disables Airtime Fairness on the selected 2.4 GHz and 5 GHz access points.

**RCI** `/rci/interface/atf/disable`

**Catch:** the positive command is the disabling operation, while its `no` form enables Airtime Fairness again.

### `interface atf inbound` — changes settings

Restricts Airtime Fairness to inbound traffic on the selected wireless access points.

**RCI** `/rci/interface/atf/inbound`

**Catch:** the example shows one invocation producing separate status messages for WifiMaster0 and WifiMaster1, so the operation may fan out across both bands; its `no` form reverses the setting.

### `interface auto-ssid` — changes settings

Builds a wireless network name by adding a MAC-address suffix to a chosen prefix.

**RCI** `/rci/interface/auto-ssid`

**Arguments:**

| Argument | Notes |
|---|---|
| `template` | `mac4` appends four MAC-address digits; `mac6` appends six. |
| `prefix` | The custom text placed before the generated suffix. |

**Catch:** the generated suffix is taken from the router MAC address, so identical prefixes can still produce different SSIDs on different routers.

### `interface backhaul` — changes settings

Enables VLAN trunk support for the wireless router-to-router backhaul.

**RCI** `/rci/interface/backhaul`

**Catch:** NONE

### `interface band-steering` — changes settings

Enables band steering for the 5 GHz access point.

**RCI** `/rci/interface/band-steering`

**Catch:** steering requires both 2.4 GHz and 5 GHz access points to be enabled with matching SSIDs and matching security settings; enabling the command alone is not sufficient.

### `interface band-steering preference` — changes settings

Selects the preferred radio band for band steering.

**RCI** `/rci/interface/band-steering/preference`

**Arguments:**

| Argument | Notes |
|---|---|
| `band` | Use `2` for 2.4 GHz or `5` for 5 GHz. |

**Catch:** no preference is defined by default, and the `no` form removes the preference rather than selecting the other band.

### `interface beamforming explicit` — changes settings

Enables explicit beamforming for the 5 GHz access point.

**RCI** `/rci/interface/beamforming/explicit`

**Arguments:**

| Argument | Notes |
|---|---|
| `mu-mimo` | Optional flag that selects MU-MIMO; omitting it selects SU-MIMO. |

**Catch:** the optional `mu-mimo` flag changes the enabled mode from SU-MIMO to MU-MIMO, while the feature is limited to 802.11ac clients and is incompatible with other standards.

### `interface beamforming implicit` — changes settings

Enables implicit beamforming for the 5 GHz access point.

**RCI** `/rci/interface/beamforming/implicit`

**Catch:** NONE

### `interface ccp` — changes settings

Enables CCP support while a connection is being established.

**RCI** `/rci/interface/ccp`

**Catch:** NONE

### `interface channel` — changes settings

Selects the radio channel or restores automatic channel selection.

**RCI** `/rci/interface/channel`

**Arguments:**

| Argument | Notes |
|---|---|
| `channel` | Numeric channels are 1–14 or 36–165; `auto` delegates channel selection to the router. |

**Catch:** the valid numeric range is split into two non-contiguous bands, so a value between 15 and 35 is not covered by the documented channel ranges.

### `interface channel auto-rescan` — changes settings

Schedules periodic automatic radio-channel scanning.

**RCI** `/rci/interface/channel/auto-rescan`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | The documented choices are 1, 6, 12, or 24 hours. |

**Catch:** the example uses the bare interval form, while the synopsis also permits an optional `hh:mm` schedule time; the block does not explain the time's default or semantics.

### `interface channel width` — changes settings

Sets the channel bandwidth and the direction in which an adjacent channel is added.

**RCI** `/rci/interface/channel/width`

**Arguments:**

| Argument | Notes |
|---|---|
| `width` | Choices are 20, 40-above, 40-below, 40-above/80, and 40-below/80 MHz; above and below select the adjacent-channel direction. |

**Catch:** NONE

### `interface compatibility` — changes settings

Selects the wireless PHY standards permitted on the radio interface.

**RCI** `/rci/interface/compatibility`

**Arguments:**

| Argument | Notes |
|---|---|
| `annex` | The permitted strings depend on the radio: B/G/N for 2.4 GHz, A/N for 5 GHz, or A/N+AC where the additional standard is supported. |

**Catch:** the accepted compatibility strings vary with the radio band and hardware capabilities rather than forming one universal list.

### `interface connect` — changes settings

Starts a connection attempt to a remote node.

**RCI** `/rci/interface/connect`

**Arguments:**

| Argument | Notes |
|---|---|
| `via` | Names the interface used to reach the remote node; PPPoE requires this argument. |

**Catch:** this is a connection-control action rather than just a stored setting: the `no` form terminates the connection, and PPPoE cannot use the command without `via`.

### `interface country-code` — changes settings

Assigns the interface a country code that affects its available radio channels.

**RCI** `/rci/interface/country-code`

**Arguments:**

| Argument | Notes |
|---|---|
| `code` | The literal country code applied to the interface. |

**Catch:** there is no `no` form, so the documented default cannot be restored through a negated command.

### `interface debug` — changes settings

Enables detailed PPP connection diagnostics.

**RCI** `/rci/interface/debug`

**Catch:** diagnostic details are written to the system log rather than returned by this command.

### `interface description` — changes settings

Assigns free-form text to the selected network interface.

**RCI** `/rci/interface/description`

**Arguments:**

| Argument | Notes |
|---|---|
| `description` | Arbitrary text associated with the interface. |

**Catch:** the example uses identical confirmation text for both assigning and deleting the description, so that message does not prove that text remains configured.

### `interface dfs zero-wait` — changes settings

Enables zero-wait DFS on a 5 GHz access-point radio.

**RCI** `/rci/interface/dfs/zero-wait`

**Catch:** NONE

### `interface down` — changes settings

Persists the network interface in the down state.

**RCI** `/rci/interface/down`

**Catch:** NONE

### `interface downlink-mumimo` — changes settings

Enables downlink explicit-beamforming MU-MIMO for a 5 GHz access point.

**RCI** `/rci/interface/downlink-mumimo`

**Catch:** The feature is restricted to 802.11ac clients, is incompatible with other standards, and cannot be enabled until `interface beamforming explicit` has been set.

### `interface downlink-ofdma` — changes settings

Enables downlink OFDMA for 802.11ax.

**RCI** `/rci/interface/downlink-ofdma`

**Catch:** NONE

### `interface duplex` — changes settings

Selects the duplex mode for an Ethernet port.

**RCI** `/rci/interface/duplex`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `full`, `half`, or `auto`; `auto` is the factory/default mode restored by `no duplex`. |

**Catch:** NONE

### `interface dyndns nobind` — changes settings

Controls whether DynDns requests are bound to the WAN interface.

**RCI** `/rci/interface/dyndns/nobind`

**Catch:** NONE

### `interface dyndns profile` — changes settings

Associates a DynDns profile with the current interface.

**RCI** `/rci/interface/dyndns/profile`

**Arguments:**

| Argument | Notes |
|---|---|
| `profile` | The name of the DynDns profile to associate. |

**Catch:** The named profile must already have been created and configured through the DynDns profile commands; this command only performs the interface association.

### `interface dyndns update` — changes settings

Manually requests a DynDns address update.

**RCI** `/rci/interface/dyndns/update`

**Arguments:**

| Argument | Notes |
|---|---|
| `force` | Bypasses the update-frequency limit recommended by the DynDns provider. |

**Catch:** A normal update observes the provider's rate policy, while adding `force` deliberately ignores that policy and can therefore trigger an update sooner than allowed by the service's recommendation.

### `interface flowcontrol` — changes settings

Controls transmit and receive Ethernet flow control.

**RCI** `/rci/interface/flowcontrol`

**Arguments:**

| Argument | Notes |
|---|---|
| `send` | Keyword selecting asynchronous send flow-control handling. |

**Catch:** The optional `send` keyword is meaningful on the `no` form: `no flowcontrol send` disables send flow control specifically, whereas the command's ordinary no-prefix form disables the feature.

### `interface follow` — changes settings

Makes an access point copy settings from a 2.4 GHz master access point.

**RCI** `/rci/interface/follow`

**Arguments:**

| Argument | Notes |
|---|---|
| `access-point` | The source access point on WifiMaster0 (2.4 GHz). |

**Catch:** Only access points whose WifiMaster index is greater than zero can follow; WifiMaster0 access points are always sources. Editing a follower terminates its link to the master.

### `interface ft enable` — changes settings

Enables IEEE 802.11r fast transition over the air for an access point.

**RCI** `/rci/interface/ft/enable`

**Catch:** Correct roaming between the 2.4 GHz and 5 GHz access points requires both to be enabled and to share the same SSID and security settings.

### `interface ft mdid` — changes settings

Sets the Mobility Domain ID used by fast transition.

**RCI** `/rci/interface/ft/mdid`

**Arguments:**

| Argument | Notes |
|---|---|
| `mdid` | Exactly two ASCII symbols. |

**Catch:** `no ft mdid` does not remove the domain ID permanently; it returns the setting to the router's default KN value.

### `interface ft otd` — changes settings

Enables 802.11r fast transition over the distribution system.

**RCI** `/rci/interface/ft/otd`

**Catch:** This is the over-the-DS variant for roaming support, distinct from the over-the-air FT option enabled by `ft enable`.

### `interface green-ethernet` — changes settings

Enables Green Ethernet mode on an Ethernet interface.

**RCI** `/rci/interface/green-ethernet`

**Catch:** NONE

### `interface hide-ssid` — changes settings

Stops an access point from advertising its SSID in wireless-network listings.

**RCI** `/rci/interface/hide-ssid`

**Catch:** Hiding the SSID does not block a client that already knows the SSID from connecting.

### `interface iapp auto` — changes settings

Generates the IAPP key automatically for the bridge.

**RCI** `/rci/interface/iapp/auto`

**Catch:** Automatic generation is the alternative to assigning a key with `interface iapp key`; the block documents no `no` form for reverting this command.

### `interface iapp key` — changes settings

Assigns the IAPP Mobile Domain key used to synchronize access points during fast transition.

**RCI** `/rci/interface/iapp/key`

**Arguments:**

| Argument | Notes |
|---|---|
| `key` | String of no more than 64 characters. |

**Catch:** The participating access points must be on the same IP subnet for this key to support synchronization.

### `interface idle-timeout` — changes settings

Sets the inactivity interval after which a station client is disconnected from an access point.

**RCI** `/rci/interface/idle-timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `idle-timeout` | Seconds from 60 through 2147483646. |

**Catch:** The documented range has no zero-value disable sentinel; disabling the setting requires the separate `no idle-timeout` form.

### `interface igmp downstream` — changes settings

Marks an IP interface as an IGMP downstream toward multicast recipients.

**RCI** `/rci/interface/igmp/downstream`

**Catch:** The device's `igmp-proxy` service must be enabled first; unlike the upstream role, the block permits several downstream interfaces.

### `interface igmp fork` — changes settings

Duplicates outgoing IGMP-upstream packets to a specified interface.

**RCI** `/rci/interface/igmp/fork`

**Catch:** Only one fork interface is permitted.

### `interface igmp upstream` — changes settings

Marks an IP interface as the IGMP upstream toward the multicast source.

**RCI** `/rci/interface/igmp/upstream`

**Catch:** The device's `igmp-proxy` service must be enabled, and only one upstream interface is allowed.

### `interface include` — changes settings

Adds an Ethernet interface as a port of a software bridge.

**RCI** `/rci/interface/include`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Name or alias of the Ethernet interface to plug into the bridge. |

**Catch:** NONE

### `interface inherit` — changes settings

Adds an Ethernet interface to a bridge while transferring selected interface settings to the bridge.

**RCI** `/rci/interface/inherit`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Name or alias of the Ethernet interface to plug into the bridge. |

**Catch:** Unlike `include`, this operation transfers the source interface's IP address, mask, and IP aliases to the bridge; removing the inheritance returns those settings to the interface and resets them on the bridge.

### `interface ipcp address` — changes settings

Controls whether the interface uses the remote peer's address.

**RCI** `/rci/interface/ipcp/address`

**Catch:** NONE

### `interface ipcp default-route` — changes settings

Controls use of the remote peer as the default gateway.

**RCI** `/rci/interface/ipcp/default-route`

**Catch:** the setting starts enabled by default, so the `no` form is an opt-out from using the peer as gateway rather than an opt-in activation.

### `interface ipcp dns-routes` — changes settings

Controls use of routes received through IPCP.

**RCI** `/rci/interface/ipcp/dns-routes`

**Catch:** NONE

### `interface ipcp name-servers` — changes settings

Controls use of DNS servers received through IPCP.

**RCI** `/rci/interface/ipcp/name-servers`

**Catch:** NONE

### `interface ipcp vj` — changes settings

Enables Van Jacobson TCP/IP-header compression on a PPP interface.

**RCI** `/rci/interface/ipcp/vj`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `cid` | Optional keyword that additionally compresses the Connection ID in headers. |

### `interface ipv6 address` — changes settings

Adds a static IPv6 address or enables stateless address autoconfiguration on an interface.

**RCI** `/rci/interface/ipv6/address`

**Catch:** the examples show several static addresses being added to the same interface, so a caller should not model the positive form as a singleton assignment.


**Arguments:**

| Argument | Notes |
|---|---|
| `address` | An IPv6 interface address. |
| `block` | An IPv6 address supplied with its mask. |
| `auto` | Enables stateless autoconfiguration. |

### `interface ipv6 dhcp client pd hint` — changes settings

Sets the prefix-delegation hint sent by the DHCPv6 client.

**RCI** `/rci/interface/ipv6/dhcp/client/pd/hint`

**Catch:** a value such as `::/64` is accepted as a length-only hint, so the zero prefix in that form is not necessarily a request for that literal delegated network.

**Arguments:**

| Argument | Notes |
|---|---|
| `prefix` | Either the requested IPv6 prefix or only its length, expressed as `::/length`. |

### `interface ipv6 id` — changes settings

Chooses how the interface identifier portion of IPv6 addresses is generated.

**RCI** `/rci/interface/ipv6/id`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `suffix` | A fixed interface-identifier suffix. |
| `eui64` | Derives the identifier from the interface MAC address. |
| `random` | Requests random identifier generation. |

### `interface ipv6 name-servers` — changes settings

Controls retrieval of DNS information through DHCPv6 name-server requests.

**RCI** `/rci/interface/ipv6/name-servers`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `auto` | Enables name-server autoconfiguration. |

### `interface ipv6 prefix` — changes settings

Configures either a manually supplied IPv6 prefix or DHCPv6 prefix delegation.

**RCI** `/rci/interface/ipv6/prefix`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `prefix` | A manually entered IPv6 prefix. |
| `auto` | Requests prefix delegation through DHCPv6-PD. |

### `interface ipv6cp` — changes settings

Enables IPv6CP while the connection is being established.

**RCI** `/rci/interface/ipv6cp`

**Catch:** NONE

### `interface lcp acfc` — changes settings

Controls negotiation of compression for PPP address and control fields.

**RCI** `/rci/interface/lcp/acfc`

**Catch:** the positive command may carry the optional `cid` mode, but the `no` form has no such argument and disables ACFC while rejecting remote ACFC requests.

**Arguments:**

| Argument | Notes |
|---|---|
| `cid` | Enables compression of the Connection ID in headers. |

### `interface lcp echo` — changes settings

Configures the interval and failure threshold for PPP LCP echo testing.

**RCI** `/rci/interface/lcp/echo`

**Catch:** reaching the unanswered-request count terminates the connection rather than merely recording a failed probe; with `adaptive`, probes are sent only after the peer has been silent since the previous probe.

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | Seconds between echo checks. |
| `count` | Number of consecutive unanswered echo requests that triggers termination. |
| `adaptive` | Sends an echo request only when no traffic from the peer has arrived since the previous request. |

### `interface lcp pfc` — changes settings

Controls negotiation of compression for the PPP protocol field.

**RCI** `/rci/interface/lcp/pfc`

**Catch:** the positive command may carry the optional `cid` mode, but the `no` form has no such argument and disables PFC while rejecting remote PFC requests.

**Arguments:**

| Argument | Notes |
|---|---|
| `cid` | Enables compression of the Connection ID in headers. |

### `interface ldpc` — changes settings

Enables or disables LDPC coding for the 5 GHz access point.

**RCI** `/rci/interface/ldpc`

**Catch:** NONE

### `interface led wan` — changes settings

Uses the LED to show the status of the selected WAN interface.

**RCI** `/rci/interface/led/wan`

**Catch:** enabling this command does not choose a WAN itself; the interface whose status is shown must first be selected through `system led`.

### `interface lldp disable` — changes settings

Turns the LLDP agent off or back on for the interface.

**RCI** `/rci/interface/lldp/disable`

**Catch:** NONE

### `interface media-type` — changes settings

Selects the operating medium for a combo RJ-45/SFP port.

**RCI** `/rci/interface/media-type`

**Catch:** `auto` is a preference order rather than an unspecified state: it prefers SFP and fails over to the RJ-45 MDI mode.

**Arguments:**

| Argument | Notes |
|---|---|
| `type` | `auto` prefers SFP with MDI failover, `mdi` forces RJ-45 operation, and `sfp` forces SFP operation. |

### `interface mobile lte disable-band` — changes settings

Keeps the list of LTE bands the mobile interface must not use.

**RCI** `/rci/interface/mobile/lte/disable-band`

**Arguments:**

| Argument | Notes |
|---|---|
| `band` | LTE band number from 1 through 43. |

**Catch:** this is a disable list: the prefixed command blocks a band, while its `no` form enables it again; the empty `no` form is a reset of the whole LTE band policy.

**Blast radius:** bare `no mobile lte disable-band` enables every LTE band.

### `interface mobile name-servers` — changes settings

Controls whether DNS addresses supplied by the mobile operator are used.

**RCI** `/rci/interface/mobile/name-servers`

**Catch:** NONE

### `interface mobile operator` — changes settings

Sets the PLMN network identifier on a USB mobile interface.

**RCI** `/rci/interface/mobile/operator`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `PLMN` | The operator identifier. |

### `interface mobile pdp` — changes settings

Selects IPv4, IPv6, or dual-stack packet data for the USB modem.

**RCI** `/rci/interface/mobile/pdp`

**Catch:** IPv6 selection depends on the corresponding system component being installed; resetting the setting selects the documented default of IPv4.

**Arguments:**

| Argument | Notes |
|---|---|
| `ipv4` | Uses IPv4 only. |
| `ipv6` | Uses IPv6 only, subject to the required system component being installed. |
| `ipv4v6` | Uses both IPv4 and IPv6. |

### `interface mobile roaming` — changes settings

Turns mobile roaming on for a USB interface.

**RCI** `/rci/interface/mobile/roaming`

**Catch:** NONE

### `interface mobile scan` — read-only

Starts a mobile-network scan on a USB interface.

**RCI** `/rci/interface/mobile/scan`

**Catch:** The scan runs for roughly 20–50 seconds and can be interrupted with `no mobile scan`; it is therefore a running operation rather than an immediate query.

### `interface mobile umts disable-band` — changes settings

Keeps the list of UMTS bands the mobile interface must not use.

**RCI** `/rci/interface/mobile/umts/disable-band`

**Arguments:**

| Argument | Notes |
|---|---|
| `band` | Only bands `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `11`, and `26` are listed as valid. |

**Catch:** the command is documented under UMTS, but both no-form examples spell the subcommand as `lte`; treat those examples as a transcription inconsistency and use the documented UMTS path when constructing the call.

**Blast radius:** the empty no-form enables every WCDMA/UMTS band.

### `interface modem connect` — changes settings

Configures the USB modem's connection sequence.

**RCI** `/rci/interface/modem/connect`

**Catch:** the modem must already have been initialized with the `tty init` command before this command is executed.

**Arguments:**

| Argument | Notes |
|---|---|
| `phone` | The number to dial. |
| `string` | An arbitrary modem command. |

### `interface modem timeout` — changes settings

Sets the USB modem connection timeout in seconds.

**RCI** `/rci/interface/modem/timeout`

**Catch:** the `no` form restores the fixed default of 30 seconds rather than leaving the current timeout unchanged.

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | An integer from 1 through 600 seconds. |

### `interface openconnect accept-addresses` — changes settings

Controls whether addresses from the OpenConnect server are accepted.

**RCI** `/rci/interface/openconnect/accept-addresses`

**Catch:** NONE

### `interface openconnect accept-routes` — changes settings

Controls whether routes received from the OpenConnect peer are accepted.

**RCI** `/rci/interface/openconnect/accept-routes`

**Catch:** NONE

### `interface openconnect authgroup` — changes settings

Sets the OpenConnect authentication group.

**RCI** `/rci/interface/openconnect/authgroup`

**Catch:** this setting is for a connection to a Cisco ASA.

**Arguments:**

| Argument | Notes |
|---|---|
| `authgroup` | The authentication group name. |

### `interface openconnect dtls` — changes settings

Controls use of DTLS for the OpenConnect connection.

**RCI** `/rci/interface/openconnect/dtls`

**Catch:** OpenConnect falls back to PPP over TLS when PPP over DTLS fails or when DTLS is disabled, so disabling this option does not necessarily prevent the connection from using TLS.

### `interface openconnect protocol fortinet` — changes settings

Enables the Fortinet protocol for OpenConnect.

**RCI** `/rci/interface/openconnect/protocol`

**Catch:** the removal command is `no openconnect protocol`, without the `fortinet` keyword, so the protocol selection is cleared at the broader `protocol` level.

### `interface openvpn accept-routes` — changes settings

Controls whether routes received from the OpenVPN peer are accepted through the tunnel.

**RCI** `/rci/interface/openvpn/accept-routes`

**Catch:** NONE

### `interface openvpn connect` — changes settings

Selects the interface used to establish the OpenVPN connection.

**RCI** `/rci/interface/openvpn/connect`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `via` | The full interface name or one of its aliases. |

### `interface openvpn name-servers` — changes settings

Controls use of DNS server addresses supplied by the OpenVPN server.

**RCI** `/rci/interface/openvpn/name-servers`

**Catch:** NONE

### `interface peer` — changes settings

Sets the remote peer or server endpoint used by the PPP connection.

**RCI** `/rci/interface/peer`

**Catch:** a server endpoint without an explicit port uses port 443, while an endpoint written as `host:port` can select another port.

**Arguments:**

| Argument | Notes |
|---|---|
| `peer` | A remote connection identifier or a server host with an optional port; the documented default port is 443. |

### `interface peer-isolation` — changes settings

Enables wireless-client isolation on the Home bridge.

**RCI** `/rci/interface/peer-isolation`

**Catch:** the setting applies to every access point included in the Bridge interface and also blocks traffic between wireless clients within the Layer 2 network.

### `interface ping-check profile` — changes settings

Assigns a Ping Check profile to the interface.

**RCI** `/rci/interface/ping-check/profile`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `profile` | The profile name to assign. |

### `interface ping-check restart` — changes settings

Enables restarting an interface when its Ping Check detects that the Internet is unavailable.

**RCI** `/rci/interface/ping-check/restart`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | The full name or alias of the interface to restart; if omitted, the interface bound to the Ping Check profile is restarted. |

### `interface pmf` — changes settings

Enables PMF for clients of a Wi-Fi access point, optionally making it mandatory under WPA2.

**RCI** `/rci/interface/pmf`

**Catch:** under WPA2 or WPA2+WPA3, plain `pmf` permits capable clients to use PMF but still allows incapable clients to connect without it; `pmf force` makes PMF mandatory, and WPA3 makes it mandatory regardless.

**Arguments:**

| Argument | Notes |
|---|---|
| `force` | Makes PMF mandatory when WPA2 encryption is used. |

### `interface pmksa-lifetime` — changes settings

Sets the lifetime of the PMK cache in minutes.

**RCI** `/rci/interface/pmksa-lifetime`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `pmksa-lifetime` | The cache lifetime in minutes. |

### `interface power` — changes settings

Sets the radio transmitter power as a percentage of its maximum.

**RCI** `/rci/interface/power`

**Catch:** the command can only reduce the hardware- and law-limited maximum, so `100` represents the permitted maximum for that radio rather than a universal absolute transmission level.

**Arguments:**

| Argument | Notes |
|---|---|
| `power` | An integer percentage from 1 through 100. |

### `interface pppoe service` — changes settings

Selects the PPPoE service to which the client connects.

**RCI** `/rci/interface/pppoe/service`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `service` | The PPPoE service name. |

### `interface pppoe session auto-cleanup` — changes settings

Controls whether an unfinished PPPoE session is closed by sending a PADT packet.

**RCI** `/rci/interface/pppoe/session/auto-cleanup`

**Catch:** NONE

### `interface preamble-short` — changes settings

Enables the short Wi-Fi preamble.

**RCI** `/rci/interface/preamble-short`

**Catch:** NONE

### `interface proxy connect` — changes settings

Starts proxy-server connection processing and optionally selects its outgoing interface.

**RCI** `/rci/interface/proxy/connect`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `via` | The interface used to reach the remote node. |

### `interface proxy protocol` — changes settings

Selects the protocol used to connect to the proxy server.

**RCI** `/rci/interface/proxy/protocol`

**Catch:** the documented `http` choice covers both HTTP and HTTPS connections, while `socks5` selects SOCKS5.

**Arguments:**

| Argument | Notes |
|---|---|
| `protocol` | `socks5` selects SOCKS5; `http` selects HTTP or HTTPS. |

### `interface proxy socks5-udp` — changes settings

Controls UDP mode for SOCKS5 proxy connections.

**RCI** `/rci/interface/proxy/socks5-udp`

**Catch:** NONE

### `interface proxy upstream` — changes settings

Sets the upstream proxy server and, optionally, its port.

**RCI** `/rci/interface/proxy/upstream`

**Catch:** NONE

**Arguments:**

| Argument | Notes |
|---|---|
| `host` | The proxy server's IP address or domain name. |
| `port` | The proxy server port. |

### `interface reconnect-delay` — changes settings

Sets the interval between PPP reconnection attempts.

**RCI** `/rci/interface/reconnect-delay`

**Catch:** the `no` form restores the documented three-second default rather than disabling reconnection attempts.

**Arguments:**

| Argument | Notes |
|---|---|
| `sec` | An integer from 3 through 600 seconds. |

### `interface rekey-interval` — changes settings

Sets the interval for automatic replacement of the shared Wi-Fi secret keys.

**RCI** `/rci/interface/rekey-interval`

**Catch:** the `no` form disables automatic key changes; it does not restore the documented 86400-second interval.

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | The rekey interval in seconds. |

### `interface rename` — changes settings

Assigns a custom name to the selected network interface.

**RCI** `/rci/interface/rename`

**Catch:** renaming the Home interface can cause unpredictable system errors, so that interface must not be renamed.

**Arguments:**

| Argument | Notes |
|---|---|
| `rename` | The new interface name. |

### `interface rf e2p set` — read-only

Writes a hexadecimal value to a calibration-data memory offset on a radio interface.

**RCI** `/rci/interface/rf/e2p/set`

**Arguments:**

| Argument | Notes |
|---|---|
| `offset` | Calibration-memory location from `1E0` through `1FE`. |
| `value` | Value written to the cell, from `0` through `FFFF`. |

**Catch:** NONE

### `interface role` — read-only

Associates a display-oriented role with an interface for VLAN-related web-interface presentation.

**RCI** `/rci/interface/role`

**Arguments:**

| Argument | Notes |
|---|---|
| `role` | The listed values are `inet`, `iptv`, `voip`, and `misc`. |
| `ifor` | Optional interface name or alias supplied after `for`. |

**Catch:** multiple roles may be assigned to one interface, and the optional `for` target lets the role refer to another interface; despite the descriptive wording, the block marks this command as not changing settings.

**Blast radius:** bare `no role` removes every role.

### `interface rrm` — changes settings

Enables RRM-based discovery of nearby access points for client-requested AP lists.

**RCI** `/rci/interface/rrm`

**Catch:** the discovered AP list is supplied to the subscriber device on request rather than being described as a continuously pushed list.

### `interface rssi-threshold` — changes settings

Sets the RSSI cutoff that controls whether an access point disconnects or rejects a Wi-Fi client.

**RCI** `/rci/interface/rssi-threshold`

**Arguments:**

| Argument | Notes |
|---|---|
| `rssi-threshold` | An RSSI value from `-100` through `0`; `0` disables the cutoff. |

**Catch:** `0` is a disable sentinel, not a threshold at the strongest end of the range.

### `interface schedule` — changes settings

Associates a previously defined schedule with an interface.

**RCI** `/rci/interface/schedule`

**Arguments:**

| Argument | Notes |
|---|---|
| `schedule` | The schedule must already have been created and configured through the schedule-action commands. |

**Catch:** Assigning a schedule is not sufficient to make it usable; the schedule must have actions configured first.

### `interface security-level` — changes settings

Assigns the interface one of the `public`, `private`, or `protected` firewall security levels.

**RCI** `/rci/interface/security-level`

**Catch:** The level is not the final filtering authority: an access list takes precedence, and private-to-protected traffic remains blocked until the global `isolate-private` setting is disabled.

### `interface sfp init-timeout` — changes settings

Sets how long the router waits for an SFP module to initialize.

**RCI** `/rci/interface/sfp/init-timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `auto` | The timeout is calculated from interface speed for non-PON modules and may instead come from the SFP quirk table. |
| `timeout` | A value in seconds from `0` through `100`. |

**Catch:** `auto` is not one fixed duration: a recognized module can receive a quirk-specific value, while other modules are calculated from speed.

### `interface sfp pcs` — changes settings

Selects the physical-coding mode used by the SFP port.

**RCI** `/rci/interface/sfp/pcs`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `fallback` cycles through several fixed modes and can take time to synchronize; the fixed modes include 1 and 2.5 Gbps variants with or without Clause 37 autonegotiation. |

**Catch:** On the KN-1011 SFP port, `100Base-FX` is unsupported, so a 100 Mbps optical link configured that way will not come up; for GPON, fallback mode cycles through its modes until synchronization.

### `interface sfp rx-los` — changes settings

Controls how the SFP port handles the receive-loss-of-signal indication.

**RCI** `/rci/interface/sfp/rx-los`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `accept` reacts to an optical-loss indication, while `ignore` permits communication without an optical cable; `auto` is detected from DDMI. |

**Catch:** Selecting `ignore` can bring up communication with no optical cable connected, rather than merely changing how a present signal loss is reported.

### `interface sim pin` — read-only

Sets the PIN used by a SIM card on a USB interface.

**RCI** `/rci/interface/sim/pin`

**Arguments:**

| Argument | Notes |
|---|---|
| `pin` | Must contain 4–8 digits; the no-form clears the configured SIM PIN. |

**Catch:** NONE

### `interface sim slot` — changes settings

Selects which SIM slot a QMI modem uses.

**RCI** `/rci/interface/sim/slot`

**Arguments:**

| Argument | Notes |
|---|---|
| `slot` | Only slot `1` or slot `2` is available. |

**Catch:** NONE

### `interface spatial-reuse` — changes settings

Enables or disables 802.11ax spatial-reuse support on the Wi-Fi master interface.

**RCI** `/rci/interface/spatial-reuse`

**Catch:** NONE

### `interface speed` — changes settings

Selects a fixed Ethernet link speed or automatic speed configuration.

**RCI** `/rci/interface/speed`

**Arguments:**

| Argument | Notes |
|---|---|
| `speed` | The fixed choices are `10`, `100`, and `1000` Mbit/s; `auto` restores automatic negotiation. |

**Catch:** NONE

### `interface speed nonegotiate` — changes settings

Disables Ethernet autonegotiation, which the block says is on by default.

**RCI** `/rci/interface/speed/nonegotiate`

**Catch:** Disabling negotiation is described for a fixed speed, so the command is not a general replacement for selecting a speed.

### `interface ssid` — changes settings

Sets the wireless network name used by an access point or Wi-Fi station.

**RCI** `/rci/interface/ssid`

**Arguments:**

| Argument | Notes |
|---|---|
| `ssid` | The network name supplied to the wireless interface. |

**Catch:** An access point cannot accept connections without an SSID, whereas a Wi-Fi station with no SSID may choose any available wireless network.

### `interface standby enable` — changes settings

Enables standby behavior for a WAN interface.

**RCI** `/rci/interface/standby/enable`

**Catch:** Standby is ignored when global priority is unset, when the interface belongs to a group such as a bridge, or when it is carrying the current WAN connection.

### `interface storm-control disable` — changes settings

Disables or reenables broadcast storm control on a bridge.

**RCI** `/rci/interface/storm-control/disable`

**Catch:** Despite `disable` being part of the command name, the bare command turns off both storm control and the loop detector; the `no` form enables both.

### `interface switchport access` — changes settings

Assigns the access VLAN ID to a switch port.

**RCI** `/rci/interface/switchport/access`

**Arguments:**

| Argument | Notes |
|---|---|
| `vid` | An access VLAN ID from `1` through `4094`. |

**Catch:** NONE

### `interface switchport friend` — changes settings

Adds a second VLAN source for downstream multicast traffic on an access port.

**RCI** `/rci/interface/switchport/friend`

**Arguments:**

| Argument | Notes |
|---|---|
| `vid` | A friend VLAN ID from `1` through `4094`. |

**Catch:** The friend VLAN is additional to the port's single access VLAN, is used only for downstream forwarding, and its packets leave untagged.

### `interface switchport mode` — changes settings

Selects access or trunk operation for a switch port, with optional double tagging in access mode.

**RCI** `/rci/interface/switchport/mode`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `access` carries untagged frames using the PVID, while `trunk` carries tagged frames from the port's VLAN membership. |
| `q-in-q` | Enables double tagging and appears as an option under `access` in the synopsis. |

**Catch:** Trunk mode does not itself define the VLAN membership; that list is configured separately with `switchport trunk`, while `q-in-q` is shown only with access mode.

### `interface switchport trunk` — changes settings

Adds a switch port to a VLAN trunk while retaining VLAN markers on transmitted frames.

**RCI** `/rci/interface/switchport/trunk`

**Arguments:**

| Argument | Notes |
|---|---|
| `vid` | VLAN ID from 1 through 4094. |

**Catch:** trunk mode permits one port to belong to several VLANs, so applying another VID adds another membership rather than replacing the existing trunk configuration.

**Blast radius:** bare `no switchport trunk vlan` removes the port from every VLAN.

### `interface target-waketime` — changes settings

Toggles 802.11ax Target Wake Time on the 2.4 GHz and 5 GHz Wi-Fi master interfaces.

**RCI** `/rci/interface/target-waketime`

**Catch:** The documented defaults differ by band: 2.4 GHz starts disabled and 5 GHz starts enabled.

### `interface traffic-shape` — changes settings

Applies an interface data-rate limit, optionally separating upstream speed and schedule.

**RCI** `/rci/interface/traffic-shape`

**Arguments:**

| Argument | Notes |
|---|---|
| `rate` | Download limit from `64` Kbps through `1` Gbps. |
| `upstream-rate` | Optional upload limit from `64` Kbps through `1` Gbps. |
| `schedule` | Optional schedule controlling when the limit applies. |

**Catch:** NONE

### `interface tty init` — changes settings

Builds the modem initialization-string list, with optional positions and per-string delays.

**RCI** `/rci/interface/tty/init`

**Arguments:**

| Argument | Notes |
|---|---|
| `index` | Optional insertion position in the initialization-string list. |
| `string` | The modem initialization text. |
| `delay` | Optional delay in seconds after the string. |

**Catch:** Initialization strings are list entries inserted at positions rather than one scalar value being overwritten.

### `interface tty send` — changes settings

Sends an AT command to a supported USB modem and waits for a matching response.

**RCI** `/rci/interface/tty/send`

**Arguments:**

| Argument | Notes |
|---|---|
| `command` | The AT command sent to the modem. |
| `expect` | Optional response pattern; the default is `OK|ERROR`. |
| `timeout` | Optional wait in seconds; the default is `3`. |

**Catch:** This is a blocking modem transaction rather than a simple stored setting: a modem can print `OK` yet the call still time out when a custom expected pattern does not match.

### `interface tunnel destination` — changes settings

Points a tunnel at its remote host.

**RCI** `/rci/interface/tunnel/destination`

**Arguments:**

| Argument | Notes |
|---|---|
| `destination` | Remote host identified by an IP address or domain name. |

**Catch:** when an automatic IPSec connection is associated with the tunnel, setting this endpoint makes the remote host initiate that IPSec connection.

### `interface tunnel eoip id` — changes settings

Assigns an identifier to an EoIP tunnel.

**RCI** `/rci/interface/tunnel/eoip/id`

**Arguments:**

| Argument | Notes |
|---|---|
| `id` | Integer tunnel identifier. |

**Catch:** the example reports that supplying `50` sets the EoIP interface to `auto`, which does not match the documented integer-ID description; treat that result as an example-specific discrepancy rather than assuming numeric input is converted to `auto`.

### `interface tunnel gre keepalive` — changes settings

Configures Cisco-style GRE keepalive probing.

**RCI** `/rci/interface/tunnel/gre/keepalive`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | Probe interval in seconds, from 0 through 60. |
| `count` | Retry count, from 1 through 20. |

**Catch:** an interval of `0` is a special mode: the router answers keepalive probes but does not use them to react to tunnel-state changes.

### `interface tunnel source` — changes settings

Selects the local side of a tunnel.

**RCI** `/rci/interface/tunnel/source`

**Arguments:**

| Argument | Notes |
|---|---|
| `auto` | Uses the currently active WAN interface. |
| `interface` | Full interface name or alias for the tunnel source. |
| `address` | IP address assigned as the tunnel's local endpoint. |

**Catch:** with an automatic IPSec connection tied to the tunnel, choosing a source activates reception of IPsec IKE connections so the secure tunnel can be established.

### `interface tx-burst` — changes settings

Enables Wi-Fi Tx Burst packet aggregation.

**RCI** `/rci/interface/tx-burst`

**Catch:** NONE

### `interface tx-queue length` — changes settings

Sets the outgoing packet queue capacity for an interface.

**RCI** `/rci/interface/tx-queue/length`

**Arguments:**

| Argument | Notes |
|---|---|
| `length` | Queue size from 0 through 65536. |

**Catch:** NONE

### `interface tx-queue scheduler cake` — changes settings

Selects CAKE as the interface's packet scheduler.

**RCI** `/rci/interface/tx-queue/scheduler/cake`

**Catch:** the bare `no` form restores the interface-specific default, so it yields CAKE on DSL or USB-modem interfaces but FQ_CODEL on other interfaces.

### `interface tx-queue scheduler fq_codel` — changes settings

Selects FQ_CODEL as the interface's packet scheduler.

**RCI** `/rci/interface/tx-queue/scheduler/fq_codel`

**Catch:** the bare `no` form restores the interface-specific default, which can be CAKE on DSL or USB-modem interfaces rather than FQ_CODEL.

### `interface up` — changes settings

Persists an interface in the enabled state.

**RCI** `/rci/interface/up`

**Catch:** enabling the interface is not merely a live-state operation: the `up` state is written to settings, while the `no` form both disables the interface and removes that persisted state.

### `interface uplink-mumimo` — changes settings

Controls 802.11ax uplink MU-MIMO.

**RCI** `/rci/interface/uplink-mumimo`

**Catch:** NONE

### `interface uplink-ofdma` — changes settings

Controls 802.11ax uplink OFDMA.

**RCI** `/rci/interface/uplink-ofdma`

**Catch:** the example labels the result as `downlink-ofdma` even though the command is `uplink-ofdma`; the block gives no rule explaining whether this is an output-label error or an actual target mismatch.

### `interface usb acq` — changes settings

Locks an NDIS modem to a selected cellular radio mode.

**RCI** `/rci/interface/usb/acq`

**Arguments:**

| Argument | Notes |
|---|---|
| `acq` | One of `gsm` (2G), `umts` (3G), `lte` (4G), or `nr5g` (5G). |

**Catch:** NONE

### `interface usb apn` — changes settings

Stores the APN used by a USB modem in NDIS mode.

**RCI** `/rci/interface/usb/apn`

**Arguments:**

| Argument | Notes |
|---|---|
| `apn` | Access point name for the modem connection. |

**Catch:** applying the APN command reboots the modem, so the setting change interrupts that modem rather than only updating configuration.

### `interface usb device-id` — changes settings

Associates vendor and model identifiers with a USB modem interface.

**RCI** `/rci/interface/usb/device-id`

**Arguments:**

| Argument | Notes |
|---|---|
| `vendor` | Vendor information used for modem matching. |
| `model` | Model information used for modem matching. |

**Catch:** matching is active: an existing `UsbModem[N]` with the supplied device ID is bound automatically, and if none exists the router creates a matching interface.

### `interface usb port-id` — changes settings

Binds a modem interface to a USB port identifier.

**RCI** `/rci/interface/usb/port-id`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | USB port identifier to bind. |
| `auto` | Requests automatic USB-port selection. |

**Catch:** `auto` is resolved to a concrete port selection rather than remaining an unspecified value; the example reports a resolved identifier, but the block does not say that this particular identifier is universal.

### `interface usb power-cycle` — read-only

Power-cycles a USB modem for a specified pause to recover it from a freeze.

**RCI** `/rci/interface/usb/power-cycle`

**Arguments:**

| Argument | Notes |
|---|---|
| `pause` | Length of the modem power-off interval, in milliseconds. |

**Catch:** NONE

### `interface usb power-fail` — changes settings

Defines the follow-up action after a modem power reset fails to recover it.

**RCI** `/rci/interface/usb/power-fail`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | Detection wait after the power reset, in seconds from 0 through 60. |
| `pause` | Disable period for the modem, in seconds from 0 through 60, when using `retry`. |
| `reboot` | Selects a complete system reboot as the recovery action. |

**Catch:** choosing `reboot` affects the entire router, not only the USB modem.

### `interface usb wwan-force-connected` — changes settings

Forces the WWAN link status instead of polling the CDC modem through HTTP.

**RCI** `/rci/interface/usb/wwan-force-connected`

**Catch:** enabling this command disables HTTP link polling via HTTP rather than merely changing an interface flag, and the `no` form removes that forced-status behavior.

### `interface vlan qos egress map` — changes settings

Maps interface egress priority values to IEEE 802.1p PCP values.

**RCI** `/rci/interface/vlan/qos/egress/map`

**Arguments:**

| Argument | Notes |
|---|---|
| `priority` | NTCE priority from 0 through 7; priority 0 applies to all outgoing packets. |
| `pcp` | Replacement IEEE 802.1p priority-code-point value. |

**Catch:** priority `0` is a wildcard for all outgoing packets, not merely the traffic class numbered zero.

### `interface web-api address` — changes settings

Sets the address used to reach a connected modem's web interface.

**RCI** `/rci/interface/web-api/address`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | IP address of the modem web interface. |

**Catch:** NONE

### `interface web-api login` — changes settings

Stores the user name for the connected modem's web interface.

**RCI** `/rci/interface/web-api/login`

**Arguments:**

| Argument | Notes |
|---|---|
| `login` | Authentication user name, up to 64 characters. |

**Catch:** NONE

### `interface web-api password` — changes settings

Stores the password for the connected modem's web interface.

**RCI** `/rci/interface/web-api/password`

**Arguments:**

| Argument | Notes |
|---|---|
| `password` | Authentication password, up to 64 characters. |

**Catch:** NONE

### `interface wmm` — changes settings

Enables WMM extensions on an interface.

**RCI** `/rci/interface/wmm`

**Catch:** NONE

### `interface wpa-eap radius secret` — changes settings

Sets the shared secret used between the RADIUS server and client.

**RCI** `/rci/interface/wpa-eap/radius/secret`

**Arguments:**

| Argument | Notes |
|---|---|
| `secret` | RADIUS shared secret, at most 64 characters. |

**Catch:** the command transcript shows the shared secret in clear text, so logging the command can disclose the RADIUS credential.

### `interface wpa-eap radius server` — changes settings

Sets the RADIUS server endpoint for the interface.

**RCI** `/rci/interface/wpa-eap/radius/server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | RADIUS server IP address. |
| `port` | Optional RADIUS server port. |

**Catch:** NONE

### `interface wps` — changes settings

Enables WPS functionality on a Wi-Fi interface.

**RCI** `/rci/interface/wps`

**Catch:** NONE

### `interface wps auto-self-pin` — changes settings

Enables automatic self-generated WPS PIN mode.

**RCI** `/rci/interface/wps/auto-self-pin`

**Catch:** auto-self-PIN mode starts enabled by default, so a newly configured interface may already have this behavior without an explicit command.

### `interface wps button` — read-only

Starts a software-button WPS session on a Wi-Fi interface.

**RCI** `/rci/interface/wps/button`

**Arguments:**

| Argument | Notes |
|---|---|
| `direction` | `send` transmits Wi-Fi configuration; `receive` obtains it from the Hero. |

**Catch:** The session ends after the first connection or after two minutes, whichever occurs first.

### `interface wps peer` — read-only

Starts a WPS session using a remote peer's PIN.

**RCI** `/rci/interface/wps/peer`

**Arguments:**

| Argument | Notes |
|---|---|
| `direction` | `send` transmits Wi-Fi configuration; `receive` obtains it from the remote peer. |
| `pin` | PIN supplied by the remote peer. |

**Catch:** WPS PIN use is disabled by default, and the session is limited to two minutes or the first connection.

### `interface wps self-pin` — read-only

Starts a WPS session using the interface's own PIN.

**RCI** `/rci/interface/wps/self-pin`

**Arguments:**

| Argument | Notes |
|---|---|
| `direction` | `send` transmits Wi-Fi configuration; `receive` obtains it from the Hero. |

**Catch:** The session ends on the first connection or after two minutes, so the command does not remain active indefinitely.

### `interface zerotier accept-addresses` — changes settings

Allows the ZeroTier server to supply addresses to the interface.

**RCI** `/rci/interface/zerotier/accept-addresses`

**Catch:** NONE

### `interface zerotier accept-routes` — changes settings

Allows routes from the remote ZeroTier side to be received.

**RCI** `/rci/interface/zerotier/accept-routes`

**Catch:** NONE

### `interface zerotier connect` — changes settings

Selects the interface used for the ZeroTier connection.

**RCI** `/rci/interface/zerotier/connect`

**Arguments:**

| Argument | Notes |
|---|---|
| `via` | Full interface name or alias used for the connection. |

**Catch:** NONE

### `interface zerotier network-id` — changes settings

Sets the network identifier for the ZeroTier tunnel.

**RCI** `/rci/interface/zerotier/network-id`

**Arguments:**

| Argument | Notes |
|---|---|
| `network-id` | ZeroTier tunnel identifier. |

**Catch:** NONE
