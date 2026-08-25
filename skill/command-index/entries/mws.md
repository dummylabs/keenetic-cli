# `mws` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `mws acquire` — read-only

Starts acquisition of an MWS candidate with optional acceptance and update flags.

**RCI** `/rci/mws/acquire`

**Arguments:**

| Argument | Notes |
|---|---|
| `candidate` | Device identifier, supplied as a MAC address or CID. |
| `eula-accept` | Requests that EULA acceptance be sent during acquisition. |
| `dpn-accept` | Requests that device-privacy-notice acceptance be sent during acquisition. |
| `no-update` | Requests acquisition without firmware-update confirmation. |

**Catch:** Acquisition is a background process: the example acknowledges that it has started, and the matching `no` command stops it for the named candidate.

### `mws auto-ap-shutdown` — changes settings

Controls automatic shutdown of Wi-Fi System Extenders when the Controller cannot be reached.

**RCI** `/rci/mws/auto-ap-shutdown`

**Catch:** the shutdown is conditional on lost Controller communication; enabling this command is not an immediate command to power off the extenders.

### `mws backhaul shutdown` — changes settings

Controls the hidden wireless backhaul access points used by MWS.

**RCI** `/rci/mws/backhaul/shutdown`

**Catch:** the documented default is enabled, so the command is an opt-out that disables hidden backhaul access points and its `no` form restores them.

### `mws log stp` — read-only

Turns STP logging on for a named interface.

**RCI** `/rci/mws/log/stp`

**Arguments:**

| Argument | Notes |
|---|---|
| `interface` | Full interface name or alias. |

**Catch:** NONE

**Blast radius:** bare `no mws log stp` disables every configured STP logger, not just one interface.

### `mws member` — read-only

Removes an MWS member by its device identifier.

**RCI** `/rci/mws/member`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device ID, either a MAC address or a CID. |

**Catch:** the example reports the removed member as pending factory reset, so treat removal as potentially queued rather than assuming immediate completion; the block does not define the timing.

**Blast radius:** bare `no mws member` clears the complete MWS-member list.

### `mws member debug` — changes settings

Enables or disables RCI debugging for one MWS member.

**RCI** `/rci/mws/member/debug`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device identifier supplied as a MAC address or CID. |

**Catch:** NONE

### `mws member dpn-accept` — read-only

Sends DPN acceptance for an MWS member.

**RCI** `/rci/mws/member/dpn-accept`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device identifier, supplied as a MAC address or CID. |

**Catch:** The example invokes the command for one CID but logs an acquisition for a different CID; that capture does not establish that the acknowledgement identifies the requested member, so do not correlate the log by ID without verification.

### `mws member port access` — changes settings

Assigns an Extender LAN port to a network segment.

**RCI** `/rci/mws/member/port/access`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Extender device ID, supplied as a MAC address or CID. |
| `port` | LAN port number. |
| `interface` | Full name of the target network segment (Bridge interface). |

**Catch:** the `no` form resets the port to the default `Bridge0` rather than merely removing the named segment; the example resets to `Bridge0` even when `Bridge2` is supplied.

### `mws member port disable` — changes settings

Takes an Extender LAN port down.

**RCI** `/rci/mws/member/port/disable`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Extender device ID, supplied as a MAC address or CID. |
| `port` | LAN port number. |

**Catch:** this is a port-state toggle: the positive form sets the port down, while `no disable` brings it back up.

### `mws member reboot` — read-only

Schedules or initiates a reboot of an MWS member.

**RCI** `/rci/mws/member/reboot`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device identifier, supplied as a MAC address or CID. |
| `interval` | Delay before reboot, from 0 to 60 seconds; omitting it requests immediate execution. |

**Catch:** With a delay, the example reports the member as pending reboot, so the command acknowledgement is not confirmation that the extender has already restarted; reboot progress is expected in `show mws member`.

### `mws member update channel` — changes settings

Selects the software update channel for an Extender.

**RCI** `/rci/mws/member/update/channel`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Extender device ID, supplied as a MAC address or CID. |
| `channel` | Update-channel name; the available names come from `components auto-update channel`. |

**Catch:** the examples show confirmations naming a MAC address different from the supplied CID; the block does not explain the mapping, so a client should not assume the confirmation echoes the member identifier.

### `mws member update check` — read-only

Requests an update check for an MWS member.

**RCI** `/rci/mws/member/update/check`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device identifier, supplied as a MAC address or CID. |

**Catch:** NONE

### `mws member update start` — read-only

Requests that an MWS member update begin.

**RCI** `/rci/mws/member/update/start`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | Device identifier, supplied as a MAC address or CID. |

**Catch:** The example reports a pending update in the automatic sandbox rather than a completed update; treat the command as a request that may still be queued.

### `mws member update stop` — read-only

Stops an update on the selected MWS member.

**RCI** `/rci/mws/member/update/stop`

**Arguments:**

| Argument | Notes |
|---|---|
| `member` | The member is identified by a MAC address or CID. |

**Catch:** NONE

---

### `mws reboot` — read-only

Requests a reboot of the complete Modular Wi-Fi System.

**RCI** `/rci/mws/reboot`

**Catch:** the request is deferred: the example reports a ten-second pending reboot rather than an immediate restart.

---

### `mws revisit` — read-only

Re-reads the status of a possible MWS member.

**RCI** `/rci/mws/revisit`

**Arguments:**

| Argument | Notes |
|---|---|
| `candidate` | The candidate is identified by a MAC address or CID. |

**Catch:** the revisit is a background operation: the positive form reports that it started, while the `no` form reports that it stopped, rather than returning the candidate's status.

---

### `mws stp encapsulation` — changes settings

Enables STP traffic encapsulation for MWS links.

**RCI** `/rci/mws/stp/encapsulation`

**Catch:** the Controller must be configured before Extenders are associated, and all previously associated Extenders must be removed first; the block recommends a direct Controller-to-Extender connection while doing this.

### `mws stp priority` — read-only

Sets the STP bridge priority, whose default is 32768.

**RCI** `/rci/mws/stp/priority`

**Arguments:**

| Argument | Notes |
|---|---|
| `priority` | One of the documented bridge-priority values from 0 through 53248. |

**Catch:** the no-prefix form resets the priority to 32768; it does not select another priority value.

---

### `mws update start` — read-only

Starts an MWS update, processing members sequentially and then the controller when both are eligible.

**RCI** `/rci/mws/update/start`

**Arguments:**

| Argument | Notes |
|---|---|
| `controller` | Restricts the request to the controller, but a member update already in progress is completed first. |
| `members` | Restricts the request to members and excludes the controller from this request. |

**Catch:** the default sequence is members first and controller second; selecting `controller` does not jump ahead of a member update that is already running. If there are no updates, the command does nothing.

---

### `mws update stop` — read-only

Stops the MWS update process.

**RCI** `/rci/mws/update/stop`

**Catch:** NONE

---

### `mws zone` — read-only

Restricts a client device to a specified MWS member.

**RCI** `/rci/mws/zone`

**Arguments:**

| Argument | Notes |
|---|---|
| `mac` | Client MAC address; it must already be listed as a known host. |
| `cid` | MWS member identifier. |

**Catch:** NONE

**Blast radius:** bare `no mws zone` clears every client-to-member zone restriction.
