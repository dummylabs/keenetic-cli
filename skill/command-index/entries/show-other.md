# `show` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `show` — read-only

Enters the command group for system diagnostics.

**RCI** `/rci/show`

**Catch:** NONE

---

### `show access` — read-only

Reports the permissions attached to a USB-directory path.

**RCI** `/rci/show/access`

**Catch:** users are emitted as repeated `user` records, so the result must be collected rather than treated as one object whose fields can be overwritten.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `directory` | String | The example addresses `PENDRIVE:doc`. |

**Returns (fields):** `user`, `name`, `assigned`, `effective`, `exists`.

### `show acme` — read-only

Reports the ACME client and certificate-account state.

**RCI** `/rci/show/acme`

**Catch:** the status combines boolean work-state flags with queue counters and timer values; a zero timer or queue size is a reported state, not evidence that the corresponding field is absent.

**Returns (fields):** `acme`, `real-time`, `ndns-domain`, `ndns-domain-acme`, `ndns-domain-error`, `default-domain`, `account-pending`, `account-running`, `get-pending`, `get-running`, `revoke-pending`, `revoke-running`, `reissue-queue-size`, `revoke-queue-size`, `retries`, `checker-timer`, `apply-timer`, `acme-account`.

### `show afp` — read-only

Reports the AFP server and its exported shares.

**RCI** `/rci/show/afp`

**Catch:** shares arrive as repeated `share` records; the example has both a whole-volume mount and a subdirectory mount, so `mount` is not a safe assumption of one record per server.

**Returns (fields):** `enabled`, `automount`, `permissive`, `share`, `mount`, `label`, `timemachine`, `description`, `active`.

### `show associations` — read-only

Lists wireless stations associated with a selected access point.

**RCI** `/rci/show/associations`

**Catch:** stations are repeated records, and the selected AP is echoed in each record; code should preserve each station record instead of flattening the repeated `station` key.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | String | The example selects `WifiMaster0/AccessPoint0`. |

**Returns (fields):** `station`, `mac`, `ap`, `authenticated`, `txrate`, `uptime`, `txbytes`, `rxbytes`, `ht`, `mode`, `gi`, `rssi`, `mcs`.

### `show button` — read-only

Reports the selected system button and its current interaction counters.

**RCI** `/rci/show/button`

**Catch:** the example nests button identity and button-state counters at different levels, so `position_count`, `clicks`, `elapsed`, and `hold_delay` belong to the button report rather than to the `button, name = …` record.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | String | The example selects `FN1`; available names depend on the device hardware. |

**Returns (fields):** `buttons`, `button`, `is_switch`, `position`, `position_count`, `clicks`, `elapsed`, `hold_delay`.

### `show button bindings` — read-only

Lists the actions assigned to device-button gestures.

**RCI** `/rci/show/button/bindings`

**Catch:** unused gesture slots are still emitted with blank `active_handler` and `default_handler` values, so an empty handler is an explicit unassigned slot rather than a missing record.

**Returns (fields):** `bindings`, `binding`, `index`, `button`, `action`, `active_handler`, `default_handler`, `protected`.

### `show button handlers` — read-only

Lists the button handlers available to the system.

**RCI** `/rci/show/button/handlers`

**Catch:** handler records carry a protection flag independently of their descriptive text; the example shows protected handlers such as `FactoryReset` and `Reboot` alongside unprotected handlers.

**Returns (fields):** `handlers`, `handler`, `short_description`, `protected`, `switch_related`.

### `show chilli profiles` — read-only

Lists the configured RADIUS service profiles available to Chilli.

**RCI** `/rci/show/chilli/profiles`

**Catch:** the `custom` key repeats three times inside one profile, each time carrying a different value (`uamsecret`, `radiussecret`, `radiusnasid`), so it is a repeated key with distinct payloads rather than one setting; a parser storing one value per key keeps only the last.

**Returns (fields):** `profile`, `name`, `url`, `description`, `preset`, `uamserver`, `radius`, `server1`, `radiuslocationid`, `dns`, `dns1`, `dns2`, `custom`.

### `show cifs` — read-only

Reports the CIFS server and its mounted share state.

**RCI** `/rci/show/cifs`

**Catch:** the flat fields describe the server while `share` opens a nested record, so `active: no` belongs to the share and not to the CIFS service; reading `active` at the top level misreports server state.

**Returns (fields):** `enabled`, `master`, `automount`, `permissive`, `share`, `mount`, `label`, `description`, `active`.

### `show clock date` — read-only

Reports the current system clock together with its timezone rule.

**RCI** `/rci/show/clock/date`

**Catch:** the clock and timezone are two sibling parts of one response, so `dst` describes the current clock state while `usesdst` and `rule` describe the timezone configuration.

**Returns (fields):** `weekday`, `day`, `month`, `year`, `hour`, `min`, `sec`, `msec`, `dst`, `tz`, `locality`, `stdoffset`, `dstoffset`, `usesdst`, `rule`, `custom`.

### `show clock timezone-list` — read-only

Enumerates the timezones the router will accept, as repeated records.

**RCI** `/rci/show/clock/timezone-list`

**Catch:** entries repeat under the same `tz` key rather than arriving as a keyed map, so a parser that assigns each key once will keep only the last timezone. Separately, the example carries `dstoffset: -1` on localities that have no daylight saving while others carry a real offset, which reads as a sentinel rather than a one-second offset — the block does not say so, so verify before relying on it.

**Returns (fields):** `timezones`, `tz`, `locality`, `stdoffset`, `dstoffset`.

### `show components status` — read-only

Reports whether the components update process is idle or active.

**RCI** `/rci/show/components/status`

**Catch:** the two captures have different shapes: the idle response has only `state`, while the running response adds `progress`; do not require `progress` for every state.

**Returns (fields):** `update`, `state`, `progress`.

### `show configurator status` — read-only

Reports configurator metadata, the serving session, and the request being processed.

**RCI** `/rci/show/configurator/status`

**Catch:** the example includes the requesting host and the parsed CLI command in the status output, so this response can disclose request-context data rather than only static configurator state.

**Returns (fields):** `touch`, `header`, `name`, `serving`, `time`, `request`, `host`, `parse`.

### `show credits` — read-only

Provides package license records or, for a selected package, its license text.

**RCI** `/rci/show/credits`

**Catch:** the example shows repeated `package` records when listing packages, whereas a package-specific call can produce a large `copying` text block; consumers must handle both repeated metadata and non-record license content.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `package` | String | Package name whose license information is requested. |

**Returns (fields):** `package`, `name`, `title`, `homepage`, `copying`.

### `show crypto ike key` — read-only

Reports the configured IKE keys and their identifiers.

**RCI** `/rci/show/crypto/ike/key`

**Catch:** IKE keys are repeated `ike_key` records identified by a displayed name, and the example shows that `id` is paired with a `type` such as `address` or `any`; do not assume every record has the same identifier semantics.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `name` | String | The example lists two differently typed keys when no key name is shown. |

**Returns (fields):** `IpSec`, `ike_key`, `name`, `type`, `id`.

### `show crypto map` — read-only

Reports an IPsec crypto map configuration and its live IKE and IPsec security-association state.

**RCI** `/rci/show/crypto/map`

**Catch:** the response mixes configuration with live phase records: `phase2_sa` is a repeated indexed record under `phase2_sa_list`, while the example also shows an empty `ipsec_dh_group` and a zero `rekey_time`, values that should be preserved rather than treated as missing data.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `map-name` | String | Name of the selected crypto map. |

**Returns (fields):** `IpSec`, `crypto_map`, `name`, `config`, `remote_peer`, `crypto_ipsec_profile_name`, `mode`, `local_network`, `net`, `mask`, `protocol`, `remote_network`, `status`, `primary_peer`, `phase1`, `unique_id`, `ike_state`, `establish_time`, `rekey_time`, `reauth_time`, `local_addr`, `remote_addr`, `ike_version`, `local_spi`, `remote_spi`, `local_init`, `ike_cypher`, `ike_hmac`, `ike_dh_group`, `phase2_sa_list`, `phase2_sa`, `index`, `request_id`, `sa_state`, `encapsulation`, `ipsec_cypher`, `ipsec_hmac`, `ipsec_dh_group`, `in_bytes`, `in_packets`, `in_time`, `out_bytes`, `out_packets`, `out_time`, `local_ts`, `remote_ts`, `state`.

### `show defaults` — read-only

Gives the router's factory wireless and service parameters, credentials included.

**RCI** `/rci/show/defaults`

**Catch:** the response carries credential fields — `servicepass`, `wlankey` and `wlanwps` — which the manual prints masked; treat this output as secret-bearing rather than ordinary defaults.

**Returns (fields):** `servicetag`, `servicehost`, `servicepass`, `wlanssid`, `wlankey`, `wlanwps`, `country`, `ndmhwid`, `product`, `ctrlsum`, `serial`, `signature`, `integrity`, `locked`.

### `show dlna` — read-only

Reports whether the DLNA server is running.

**RCI** `/rci/show/dlna`

**Catch:** NONE

**Returns (fields):** `running`.

### `show dns-proxy` — read-only

Reports the configured DNS proxy profiles and their current resolver statistics.

**RCI** `/rci/show/dns-proxy`

**Catch:** the output mixes `key: value` records, `key = value` configuration lines, and a formatted DNS-server statistics table; repeated resolver entries use the same keys, so a parser must preserve record order and must not treat the whole response as one uniform map.

**Returns (fields):** `proxy-status`, `proxy-name`, `proxy-config`, `rpc_port`, `rpc_ttl`, `rpc_wait`, `timeout`, `proceed`, `stat_file`, `stat_time`, `dns_server`, `static_a`, `set-profile-ip`, `dns_tcp_port`, `dns_udp_port`, `proxy-stat`, `Total incoming requests`, `Proxy requests sent`, `Cache hits ratio`, `Memory usage`, `proxy-safe`, `proxy-tls`, `server-tls`, `address`, `port`, `sni`, `spki`, `interface`, `proxy-tls-filters`, `proxy-https`, `server-https`, `uri`, `format`, `proxy-https-filters`.

**Returns (text table columns):** `Ip`, `Port`, `R.Sent`, `A.Rcvd`, `NX.Rcvd`, `Med.Resp`, `Avg.Resp`, `Rank`.

### `show dns-proxy filter presets` — read-only

Lists the filtering presets and their localized descriptions.

**RCI** `/rci/show/dns-proxy/filter/presets`

| Argument | Type | Notes |
|---|---|---|
| `lang` | String | Selects the language for the two description fields. |

**Catch:** requesting an unavailable language does not leave those descriptions absent; the block says the English version is used instead. Presets are repeated records under `presets`, not a map keyed by `id`; `stale` marks a preset that is obsolete and no longer works.

**Returns (fields):** `version`, `presets`, `id`, `url`, `stale`, `short-description`, `description`.

### `show dns-proxy filter profiles` — read-only

Lists the configured DNS filtering profiles.

**RCI** `/rci/show/dns-proxy/filter/profiles`

**Catch:** NONE

**Returns (fields):** `profiles`, `id`, `description`.

### `show dot1x` — read-only

Reports 802.1X client state for an Ethernet interface.

**RCI** `/rci/show/dot1x`

| Argument | Type | Notes |
|---|---|---|
| `interface` | Interface | Applies to Ethernet interfaces; the interface authentication group must already be configured to manage this status. |

**Catch:** without the interface authentication configuration, the command cannot be used to manage 802.1X status; the example's `id` is the Ethernet interface name while the queried interface is an alias.

**Returns (fields):** `dot1x`, `id`, `state`.

### `show dpn document` — read-only

Retrieves the selected device privacy notice text.

**RCI** `/rci/show/dpn/document`

| Argument | Type | Notes |
|---|---|---|
| `version` | String | Omission selects the latest available version. |
| `language` | String | Omission selects English. |

**Catch:** the result is document text rather than a field map, and the requested version and language are rendered as part of the document response rather than exposed through a structured output schema.

### `show dpn list` — read-only

Enumerates the available device privacy notice versions, languages, and formats.

**RCI** `/rci/show/dpn/list`

**Catch:** `document` is repeated for each language and `format` is repeated within each document, so a parser that treats either key as singular will lose entries.

**Returns (fields):** `dpn`, `version`, `document`, `lang`, `format`.

### `show drivers` — read-only

Lists the kernel drivers currently loaded.

**RCI** `/rci/show/drivers`

**Catch:** driver records repeat under `module`, and `subs` is not uniform: the example shows both `-` and a dependency string containing `[permanent]`; do not assume it is always a list or always empty.

**Returns (fields):** `module`, `name`, `size`, `used`, `subs`.

### `show dyndns updaters` — read-only

Lists the DynDNS providers available to the router.

**RCI** `/rci/show/dyndns/updaters`

**Catch:** NONE

**Returns (fields):** `updater`, `type`, `url`, `api`.

### `show easyconfig status` — read-only

Reports EasyConfig reachability checks and the selected gateway and hosts.

**RCI** `/rci/show/easyconfig/status`

**Catch:** the status is hierarchical: gateway data and host test records are nested beneath the EasyConfig result, and a host can be unresolved and inaccessible even while the gateway and broader connectivity checks are accessible.

**Returns (fields):** `easyconfig`, `checked`, `enabled`, `reliable`, `gateway-accessible`, `dns-accessible`, `host-accessible`, `internet`, `gateway`, `interface`, `address`, `failures`, `accessible`, `excluded`, `hosts`, `host`, `name`, `resolved`.

### `show eula document` — read-only

Retrieves the selected end-user licence agreement text.

**RCI** `/rci/show/eula/document`

| Argument | Type | Notes |
|---|---|---|
| `version` | String | Omission selects the latest available version. |
| `language` | String | Omission selects English. |

**Catch:** the result is document text rather than a field map, and the selected version and language appear in the rendered text instead of a structured response schema.

### `show eula list` — read-only

Enumerates the available end-user licence agreement versions, languages, and formats.

**RCI** `/rci/show/eula/list`

**Catch:** `document` is repeated per language and `format` is repeated within each document, so these records must be accumulated rather than stored as single values.

**Returns (fields):** `eula`, `version`, `document`, `lang`, `format`.

### `show internet status` — read-only

Checks reachability of the gateway, DNS, test hosts, and the resulting internet status.

**RCI** `/rci/show/internet/status`

**Catch:** the aggregate `internet` result can be positive even when an individual host check is not: the example reports `internet: yes` while one listed host has `resolved: no` and `accessible: no`; the block does not define how the aggregate is derived.

**Returns (fields):** `checked`, `reliable`, `gateway-accessible`, `dns-accessible`, `host-accessible`, `internet`, `gateway`, `interface`, `address`, `failures`, `accessible`, `excluded`, `hosts`, `host`, `name`, `resolved`.

### `show ipsec` — read-only

Reports the status and current associations of the IPsec/IKE service.

**RCI** `/rci/show/ipsec`

**Catch:** this is a human-readable diagnostic report rather than a uniform record set: it includes free-form daemon text, lists of listening addresses and connections, and association lines whose details vary with state. Do not parse the whole response as one flat field map.

**Returns (fields):** `ipsec_statusall`, `uptime`, `worker threads`, `loaded plugins`.

**Returns (report labels):** `Status of IKE charon daemon`, `Listening IP addresses`, `Connections`, `Security Associations`.

### `show ipv6 addresses` — read-only

Lists the IPv6 addresses currently reported by the router.

**RCI** `/rci/show/ipv6/addresses`

**Catch:** the response contains repeated `address` records rather than one address-keyed map, so a parser must retain every record.

**Returns (fields):** `address`, `interface`, `valid-lifetime`.

### `show ipv6 dhcp bindings` — read-only

Reports DHCPv6 subnets and their active leases.

**RCI** `/rci/show/ipv6/dhcp/bindings`

**Catch:** lease records are not uniform: the example's IA-NA lease has `address`, while its IA-PD lease has `prefix` and `remote`; code must branch on the lease type instead of requiring one fixed payload.

**Returns (fields):** `subnet`, `name`, `lease`, `type`, `duid`, `address`, `expires`, `prefix`, `remote`.

### `show ipv6 prefixes` — read-only

Lists the IPv6 prefixes currently known to the router.

**RCI** `/rci/show/ipv6/prefixes`

**Catch:** the example contains multiple `prefix` records, and the `interface` value is empty on two of them; do not assume every returned prefix is associated with a nonempty interface.

**Returns (fields):** `prefix`, `interface`, `valid-lifetime`, `preferred-lifetime`.

### `show ipv6 route` — read-only

Lists IPv6 routes, optionally selecting a table or a sort order.

**RCI** `/rci/show/ipv6/route`

| Argument | Notes |
|---|---|
| `table` | The example selects table `42`. |
| `criteria` | Sorting can use `interface`, `gateway`, or `destination`. |
| `direction` | Sorting can be `ascending` or `descending`. |

**Catch:** the same displayed destination appears with `proto: boot` in the table query and `proto: kernel` in the interface-sorted query; the block does not explain that difference, so consumers should not treat `proto` as stable across invocations.

**Returns (fields):** `route6`, `destination`, `gateway`, `interface`, `metric`, `flags`, `rejecting`, `proto`, `floating`, `static`.

### `show ipv6 subnets` — read-only

Lists IPv6 subnets together with their associated prefixes.

**RCI** `/rci/show/ipv6/subnets`

**Catch:** the example's subnet has `interface: Home`, but its nested prefix has `interface: TunnelSixInFour0`; use the prefix-level interface rather than inheriting the subnet's interface.

**Returns (fields):** `subnet`, `name`, `prefixes`, `prefix`, `interface`, `valid-lifetime`, `preferred-lifetime`, `global`.

### `show kabinet status` — read-only

Reports the КАБiNET authenticator's enablement, connection, and protocol state.

**RCI** `/rci/show/kabinet/status`

**Catch:** the example reports `enabled: yes` and `wan: yes` while `state` is `STOPPED`, so enabled or WAN-ready must not be interpreted as currently running.

**Returns (fields):** `kabinet`, `enabled`, `wan`, `state`, `server`, `access-level`, `protocol-version`.

### `show last-change` — read-only

Reports the recorded time and agent for the latest settings change.

**RCI** `/rci/show/last-change`

**Catch:** NONE

**Returns (fields):** `date`, `agent`.

### `show led` — read-only

Reports information about one LED or the available LED set.

**RCI** `/rci/show/led`

| Argument | Notes |
|---|---|
| `name` | The example uses `FN_1`, although the argument listing shows `FN`; do not assume the displayed list is exhaustive. |

**Catch:** the example's requested `FN_1` identifier is not written exactly as `FN` in the documented value list, so callers should not reject such device-specific names solely from that list.

**Returns (fields):** `leds`, `led, index = 0`, `name`, `user_configurable`, `virtual`.

### `show led bindings` — read-only

Reports the control binding associated with each LED.

**RCI** `/rci/show/led/bindings`

| Argument | Notes |
|---|---|
| `name` | The LED selector; the example omits it and lists bindings. |

**Catch:** the `FW_UPD` record has both `active_control` and `default_control` empty even though it is present and not user-configurable; empty control values are therefore a valid observed case.

**Returns (fields):** `bindings`, `binding, index = 0`, `led`, `user_configurable`, `active_control`, `default_control`.

### `show led controls` — read-only

Lists the LED controls available on the device.

**RCI** `/rci/show/led/controls`

**Catch:** the available control list is hardware-dependent, so a caller must tolerate controls being absent on another device.

**Returns (fields):** `controls`, `control, index = 0`, `name`, `short_description`, `owner`, `user_configurable`.

### `show log` — read-only

Streams records from the system's circular log buffer.

**RCI** `/rci/show/log`

**Catch:** without `once`, the command remains active in the background and continues until the user interrupts it with Ctrl+C; `once` is the explicit form that prints the current log and returns to the CLI.

**Arguments:**

| Argument | Notes |
|---|---|
| `max-lines` | Limits the number of returned log items. |
| `once` | Requests a single current-log dump instead of the continuing command. |

**Returns (text table columns):** `Time`, `Message`.

### `show media` — read-only

Reports attached USB media and their partitions.

**RCI** `/rci/show/media`

**Catch:** the swap partition in the example carries an all-zero UUID, so UUID should not be assumed to be a meaningful nonzero identifier for every partition.

**Returns (fields):** `media`, `name`, `port`, `state`, `manufacturer`, `product`, `serial`, `size`, `partition`, `uuid`, `label`, `fstype`, `total`, `free`.

### `show mws associations` — read-only

Lists Access Point associations reported by MWS repeaters.

**RCI** `/rci/show/mws/associations`

**Catch:** NONE

**Returns (fields):** `station`, `mac`, `ap`, `authenticated`, `txrate`, `rxrate`, `uptime`, `txbytes`, `rxbytes`, `ht`, `mode`, `gi`, `rssi`, `mcs`, `txss`, `ebf`, `mu`.

### `show mws candidate` — read-only

Lists MWS candidates or describes a selected candidate by device identifier.

**RCI** `/rci/show/mws/candidate`

| Argument | Notes |
|---|---|
| `candidate` | A device ID, documented as either a MAC address or CID. |

**Catch:** the example shows an empty `rci` section and four repeated `port` records containing only `label`; parsers must allow those sections to exist without further values.

**Returns (fields):** `candidate`, `mac`, `cid`, `mode`, `model`, `state`, `fw`, `fw-available`, `license`, `eula-accepted`, `dpn-accepted`, `stp-encapsulation`, `port`, `label`, `rci`.

### `show mws log` — read-only

Streams MWS association and transition events until the user interrupts it.

**RCI** `/rci/show/mws/log`

| Argument | Notes |
|---|---|
| `max-lines` | Limits the number of displayed log entries. |
| `once` | Requests recent entries in the captured example. |

**Catch:** this command runs in the background and does not finish on its own; a caller must handle an interrupt-driven stream rather than wait for an ordinary one-shot response.

**Returns (text table columns):** `Time`, `Message`.

### `show mws member` — read-only

Lists MWS members or describes one selected by its device identifier.

**RCI** `/rci/show/mws/member`

| Argument | Notes |
|---|---|
| `member` | A device ID, documented as either a MAC address or CID. |

**Catch:** the example includes a `license` identifier and a capability named `auth-token`, alongside cloud and backhaul state; treat the returned member description as sensitive inventory data rather than a minimal status record.

**Returns (fields):** `member`, `cid`, `model`, `mac`, `known-host`, `ip`, `mode`, `hw_type`, `hw_id`, `license`, `fqdn`, `fqdn-certificate-valid`, `cloud-agent-state`, `internet-available`, `fw`, `fw-available`, `fw-release`, `fw-release-available`, `fw-update-available`, `fw-update-sandbox`, `region`, `associations`, `capabilities`, `acme`, `auth-token`, `auto-ap-shutdown`, `backhaul-bss`, `cloud`, `controller`, `comp-status`, `country-code`, `dual-band`, `mac-band`, `mode-hw`, `mws-assoc`, `new-commit`, `notify`, `owe`, `seg-band-steering`, `sta-mask`, `wind`, `wpa3`, `wpa-eap`, `vht40`, `stp-encapsulation`, `new-password-api`, `security-level`, `cloud-control2`, `interface`, `system`, `cpuload`, `memory`, `uptime`, `backhaul`, `uplink`, `root`, `bridge`, `cost`, `ap`, `psm`, `mld`, `authenticated`, `txrate`, `ht`, `gi`, `rssi`, `mcs`, `txss`, `ebf`, `dl-mu`, `ul-mu`, `dl-ofdma`, `pmf`, `security`, `port`, `label`, `appearance`, `link`, `speed`, `duplex`, `rci`, `errors`.

### `show ndns` — read-only

Reports the latest KeenDNS request parameters and the associated tunnel details.

**RCI** `/rci/show/ndns`

**Catch:** the example contains wildcard tunnel values such as `client: *` and `target: *:80`, as well as zero addresses; the block does not define these values, so they must not be treated as ordinary concrete endpoints without verification.

**Returns (fields):** `name`, `booked`, `domain`, `address`, `address6`, `updated`, `access`, `access6`, `xns`, `ttp`, `direct`, `interface`, `tunnel`, `client`, `target`, `target-local`, `target-remote`, `default-fqdn`, `destination`, `dialback`, `timeout`, `uptime`, `idle`, `linger`.

### `show netfilter` — read-only

Provides firewall diagnostics intended for remote technical support.

**RCI** `/rci/show/netfilter`

**Catch:** NONE

### `show nextdns availability` — read-only

Reports whether NextDNS and its DNS-over-HTTPS path are available.

**RCI** `/rci/show/nextdns/availability`

**Catch:** NONE

**Returns (fields):** `available`, `port`, `doh-supported`, `doh-available`.

### `show nextdns profiles` — read-only

Lists the NextDNS profiles loaded by the client.

**RCI** `/rci/show/nextdns/profiles`

**Catch:** profiles repeat under the same `profile` record key rather than forming a map, and the example gives the no-filtering profile a token of `0`; preserve repeated records and do not assume every token is a nonzero profile identifier.

**Returns (fields):** `profiles`, `profile`, `name`, `token`.

### `show ntp status` — read-only

Reports synchronization timing and the current NTP state indicators.

**RCI** `/rci/show/ntp/status`

**Catch:** `accurate` and `synchronized` are separate status indicators, while `ndsstime` and `usertime` identify different time sources; none of these fields should be collapsed into one generic “time synced” flag.

**Returns (fields):** `status`, `elapsed`, `server`, `accurate`, `synchronized`, `ndsstime`, `usertime`.

### `show object-group fqdn` — read-only

Inspects an FQDN object group, including resolved entries and excluded addresses.

**RCI** `/rci/show/object-group/fqdn`

**Catch:** entries are distinguished by `type`: the example's `runtime` entries carry resolved IPv4/IPv6 address records, whereas its `config` entry has empty `ipv4` and `ipv6` sections. The config entry also shows very large `deadline4` and `deadline6` values; this is an observation from the example, not a documented sentinel.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `group` | String | Selects an FQDN object group. |

**Returns (fields):** `group`, `group-name`, `enabled`, `ipv4-addresses`, `ipv6-addresses`, `entry`, `fqdn`, `type`, `deadline4`, `deadline6`, `fail-counter4`, `fail-counter6`, `parent`, `ipv4`, `address`, `ttl`, `last-updated`, `ipv6`, `excluded-ipv4`, `excluded-ipv6`.

### `show oc-server` — read-only

Reports the OpenConnect server identity and current tunnel statistics.

**RCI** `/rci/show/oc-server`

**Catch:** the response includes the server `secret` in clear text in the example, so output handling must treat this command as secret-bearing rather than ordinary status data.

**Returns (fields):** `ndns-name`, `fqdn`, `secret`, `has-ndns-certificate`, `tunnel`, `clientaddress`, `username`, `uptime`, `statistic`, `rxpackets`, `rx-multicast-packets`, `rx-broadcast-packets`, `rxbytes`, `rxerrors`, `rxdropped`, `txpackets`, `tx-multicast-packets`, `tx-broadcast-packets`, `txbytes`, `txerrors`, `txdropped`, `timestamp`, `last-overflow`.

### `show ping-check` — read-only

Reports the status of one or all Ping Check profiles.

**RCI** `/rci/show/ping-check`

**Catch:** profile records are sparse: the example's `connect` profile has host, port, thresholds, interface, failure count, and status, while the two `icmp` profiles carry only their profile and mode. Consumers must not assume those fields exist for every mode.

**Arguments:**

| Argument | Type | Notes |
|---|---|---|
| `profile_name` | String | Selects a profile. |

**Returns (fields):** `pingcheck`, `profile`, `host`, `port`, `max-fails`, `timeout`, `mode`, `interface`, `fail count`, `status`.

### `show printers` — read-only

Lists printers attached to the router.

**RCI** `/rci/show/printers`

**Catch:** NONE

**Returns (fields):** `printers`, `printer`.

### `show processes` — read-only

Reports per-process resource and service state, with CPU statistics attached to each process record.

**RCI** `/rci/show/processes`

**Catch:** `arg` is repeated within a process record when the process has multiple arguments, so a
parser that stores one value per key will lose arguments; the example also contains multiple
`process` records.

**Returns (fields):** `process`, `id`, `name`, `arg`, `state`, `pid`, `ppid`, `vm-size`, `vm-data`, `vm-stk`, `vm-exe`, `vm-lib`, `vm-swap`, `threads`, `fds`, `statistics`, `interval`, `cpu`, `now`, `min`, `max`, `avg`, `cur`, `service`, `configured`, `alive`, `started`.

### `show running-config` — read-only

Prints the router's current running configuration as CLI configuration text.

**RCI** `/rci/show/running-config`

**Catch:** the example includes secrets in the configuration output, including Wi-Fi authentication values and IAPP keys, as well as identifying metadata such as the username; this output must be treated as sensitive rather than safe diagnostic text.

### `show schedule` — read-only

Lists the configured schedules and their timed actions.

**RCI** `/rci/show/schedule`

**Catch:** action records do not necessarily have the same fields: the example includes `next`
on one action but not the other, so consumers should treat it as conditional rather than required.

**Arguments:**

| Argument | Value | Notes |
|---|---|---|
| `name` | String | Selects a schedule by name. |

**Returns (fields):** `schedule`, `name`, `action`, `type`, `left`, `next`, `dow`, `time`.

### `show self-test` — read-only

Provides a summary intended for remote technical support.

**RCI** `/rci/show/self-test`

**Catch:** NONE

### `show site-survey` — read-only

Scans the selected wireless interface and prints the networks it can see.

**RCI** `/rci/show/site-survey`

**Catch:** the example lays out each result across wrapped text lines, with the mode and quality
value appearing below the SSID/MAC/channel row, so parsing one physical line as one network will
misassociate columns; the block does not define a machine-readable row delimiter.

**Arguments:**

| Argument | Value | Notes |
|---|---|---|
| `name` | Interface | The interface to scan. |

**Returns (text table columns):** `SSID`, `MAC`, `Ch`, `Mode`, `Q`.

### `show snmp view` — read-only

Reports the active SNMP view and its include/exclude subtrees.

**RCI** `/rci/show/snmp/view`

**Catch:** NONE

**Returns (fields):** `view`, `id`, `include`, `exclude`.

### `show ssh fingerprint` — read-only

Lists the current SSH server fingerprints for its host-key algorithms.

**RCI** `/rci/show/ssh/fingerprint`

**Catch:** each algorithm label is repeated for the MD5, SHA1, and SHA256 fingerprints, so the
algorithm alone is not a unique key and a single-value map will discard two of the three hashes.

**Returns (fields):** `rsa`, `ecdsa`.

### `show ssh sftp` — read-only

Reports SFTP availability and the home-directory settings for tagged users.

**RCI** `/rci/show/ssh/sftp`

**Catch:** the example has global `root` and `path` values as well as a repeated `user` record,
whose `root` is empty and whose `path` is shown with a `►` marker; do not assume every user record
contains a populated path or root.

**Returns (fields):** `enabled`, `permissive`, `root`, `path`, `user`, `index`, `name`.

### `show sstp-server` — read-only

Reports the SSTP server state together with the current tunnel and traffic counters.

**RCI** `/rci/show/sstp-server`

**Catch:** NONE

**Returns (fields):** `enabled`, `ndns-name`, `has-ndns-certificate`, `tunnel`, `clientaddress`, `username`, `uptime`, `statistic`, `rxpackets`, `rx-multicast-packets`, `rx-broadcast-packets`, `rxbytes`, `rxerrors`, `rxdropped`, `txpackets`, `tx-multicast-packets`, `tx-broadcast-packets`, `txbytes`, `txerrors`, `txdropped`, `timestamp`, `last-overflow`.

### `show system` — read-only

Reports the router's general system state, including resource usage and uptime.

**RCI** `/rci/show/system`

**Catch:** NONE

**Returns (fields):** `hostname`, `domainname`, `cpuload`, `memory`, `swap`, `uptime`.

### `show system country` — read-only

Shows the factory and selected country settings followed by the countries supported by the device.

**RCI** `/rci/show/system/country`

**Catch:** `default-language` occurs both at the top level and inside repeated `country` records,
so its meaning depends on the surrounding record; code that flattens by key can conflate the
device setting with a country's default.

**Returns (fields):** `factory`, `selected`, `default-language`, `country`, `code`, `short-name`.

### `show system cpustat` — read-only

Reports current, minimum, maximum, and average CPU usage for each CPU-time category.

**RCI** `/rci/show/system/cpustat`

**Catch:** NONE

**Returns (fields):** `interval`, `busy`, `user`, `nice`, `system`, `iowait`, `irq`, `sirq`, `cur`, `min`, `max`, `avg`.

### `show system zram` — read-only

Reports the configured zRam swap algorithm, sizes, compression, and thread count.

**RCI** `/rci/show/system/zram`

**Catch:** NONE

**Returns (fields):** `zram`, `enabled`, `compression-algo`, `disk-size`, `compressed-size`, `original-size`, `total-memory-used`, `compression-threads`, `compressed-ratio-pcs`.

### `show tags` — read-only

Enumerates the authentication tags available on the router.

**RCI** `/rci/show/tags`

**Catch:** every result is emitted under the same `tag` key, so treating the output as a map keeps
only the last tag instead of the complete list.

**Returns (fields):** `tag`.

### `show threads` — read-only

Lists active NDM threads with lock and CPU-statistics information.

**RCI** `/rci/show/threads`

**Catch:** `thread` is a repeated record key, and the example shows separate records with distinct
names and TIDs; collect the records rather than overwriting them by key.

**Returns (fields):** `thread`, `name`, `tid`, `lock_list_complete`, `locks`, `statistics`, `interval`, `cpu`, `now`, `min`, `max`, `avg`, `cur`.

### `show torrent status` — read-only

Reports whether the BitTorrent client is running and which RPC port it uses.

**RCI** `/rci/show/torrent/status`

**Catch:** NONE

**Returns (fields):** `state`, `rpc-port`.

### `show upnp redirect` — read-only

Lists or filters the UPnP port-translation entries.

**RCI** `/rci/show/upnp/redirect`

**Catch:** the example shows a description containing `192.168.12.286`, which is not constrained
to address syntax by the block; treat `description` as opaque text rather than parsing it as an IP
address.

**Arguments:**

| Argument | Value | Notes |
|---|---|---|
| `protocol` | `tcp` or `udp` | Part of the protocol/interface/port filter. |
| `interface` | Interface | Part of the protocol/interface/port filter. |
| `port` | Integer | Part of the protocol/interface/port filter. |
| `index` | Integer | Selects a rule by its list number instead of using the three-part filter. |

**Returns (fields):** `entry`, `index`, `interface`, `protocol`, `port`, `to-address`, `to-port`, `description`, `packets`, `bytes`.

### `show usb` — read-only

Enumerates the USB devices and their storage labels and subsystems.

**RCI** `/rci/show/usb`

**Catch:** `device` records repeat, and the example uses different identifier formats for `name`
(some hardware-like IDs and one UUID-like value), so neither the record key nor a presumed name
format is sufficient for parsing the list.

**Returns (fields):** `device`, `name`, `label`, `subsystem`.

### `show version` — read-only

Reports firmware, build, hardware, vendor, and feature information.

**RCI** `/rci/show/version`

**Catch:** NONE

**Returns (fields):** `release`, `sandbox`, `title`, `arch`, `ndm`, `exact`, `cdate`, `bsp`, `ndw`, `features`, `components`, `ndw3`, `version`, `ndw4`, `manufacturer`, `vendor`, `series`, `model`, `hw_version`, `hw_type`, `hw_id`, `device`, `consent`, `region`, `description`.

### `show vpn-server` — read-only

Reports the current VPN-server tunnel and its receive/transmit statistics.

**RCI** `/rci/show/vpn-server`

**Catch:** NONE

**Returns (fields):** `tunnel`, `clientaddress`, `username`, `uptime`, `statistic`, `rxpackets`, `rx-multicast-packets`, `rx-broadcast-packets`, `rxbytes`, `rxerrors`, `rxdropped`, `txpackets`, `tx-multicast-packets`, `tx-broadcast-packets`, `txbytes`, `txerrors`, `txdropped`, `timestamp`, `last-overflow`.
