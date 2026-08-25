# `system` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `system` — read-only

Enters the command group for global system parameters.

**RCI** `/rci/system`

**Catch:** NONE

---

### `system button` — changes settings

Binds device-button events to selected action handlers.

**RCI** `/rci/system/button`

**Arguments:**

| Argument | Notes |
|---|---|
| `button` | `RESET`, `WLAN`, `FN1`, or `FN2`. |
| `action` | `click`, `double-click`, or `hold`; a hold is 3 seconds except a RESET hold is 10 seconds. |
| `handler` | `FactoryReset`, `Reboot`, `WifiToggle`, `WifiGuestApToggle`, `WpsStartMainAp`, `WpsStartMainAp5`, `WpsStartAllMainAp`, `UnmountAll`, `DlnaDirectoryRescan`, `DlnaDirectoryFullRescan`, `TorrentAltSpeedToggle`, `TorrentClientStateToggle`, or `OpkgRunScript`; some require the corresponding installed component. |

**Catch:** Available handlers depend on the hardware configuration and installed modules, so a syntactically valid binding may not be available on every device.


**Destructive:** Choosing `FactoryReset`, `Reboot`, or `UnmountAll` assigns a system-wide action to a physical button; the block does not state what configuration or data survives those actions.

### `system caption` — changes settings

Selects the template used for the Web interface title and header.

**RCI** `/rci/system/caption`

**Arguments:**

| Argument | Notes |
|---|---|
| `template` | `default`, `product`, `description`, `hwid`, `hostname`, `ndns-domain`, or `default-ssid`; each selects the corresponding displayed device identity or name. |

**Catch:** NONE

### `system clock date` — changes settings

Adjusts the system date and time.

**RCI** `/rci/system/clock/date`

**Arguments:**

| Argument | Notes |
|---|---|
| `date-and-time` | Current date and time in `DD MM YYYY HH:MM:SS` format. |

**Catch:** NONE

### `system clock timezone` — changes settings

Selects the system timezone by locality.

**RCI** `/rci/system/clock/timezone`

**Arguments:**

| Argument | Notes |
|---|---|
| `locality` | City name whose timezone is selected. |

**Catch:** the `no` form restores GMT rather than removing only a named locality.

---

### `system configuration factory-reset` — changes settings

Restores the configuration to factory values across all system modes.

**RCI** `/rci/system/configuration/factory-reset`

**Catch:** NONE

**Destructive:** the configuration for every mode is replaced by factory settings; the block does not state what other data survives.

---

### `system configuration fail-safe commit` — read-only

Commits pending configuration changes and ends the fail-safe timer.

**RCI** `/rci/system/configuration/fail-safe/commit`

**Catch:** this is a global commit of all unsaved changes, not a selective commit; it also stops the fail-safe timer.

---

### `system configuration fail-safe keep-alive` — read-only

Refreshes the fail-safe timer without producing a normal status message.

**RCI** `/rci/system/configuration/fail-safe/keep-alive`

**Catch:** when fail-safe mode is inactive or there are no pending configuration changes, the command has no effect.

---

### `system configuration fail-safe rollback` — read-only

Discards pending configuration changes and reboots the system into its rollback state.

**RCI** `/rci/system/configuration/fail-safe/rollback`

**Catch:** the reboot enters a special state in which commit and timer-reconfiguration actions are blocked, except for disabling the timer; with no pending changes, the command does nothing.

---

### `system configuration fail-safe timer` — changes settings

Configures a reboot fail-safe timer for router mode.

**RCI** `/rci/system/configuration/fail-safe/timer`

**Arguments:**

| Argument | Notes |
|---|---|
| `action` | The documented action is `reboot`. |
| `interval` | Integer number of seconds from 60 through 86400. |

**Catch:** the timer state persists across reboots without an explicit save, and the feature is implemented only in router mode.

---

### `system configuration save` — changes settings

Starts an asynchronous save of the system configuration.

**RCI** `/rci/system/configuration/save`

**Catch:** the command returns while saving is still in progress, so completion cannot be inferred from command return alone.

**Destructive:** saving makes the current system configuration persistent; the block does not state what previous saved state or other data survives.

---

### `system country` — changes settings

Selects the country code used by the system.

**RCI** `/rci/system/country`

**Arguments:**

| Argument | Notes |
|---|---|
| `country` | Must be an ISO 3166-1 alpha-2 country code. |

**Catch:** the selection is stored persistently without a save command and affects every system mode.

---

### `system debug` — changes settings

Enables system debug mode.

**RCI** `/rci/system/debug`

**Catch:** NONE

---

### `system description` — changes settings

Sets the system description string.

**RCI** `/rci/system/description`

**Arguments:**

| Argument | Notes |
|---|---|
| `description` | Limited to 256 bytes; the default shown by the block is `Hero (KN-1011)`. |

**Catch:** the size limit is measured in bytes rather than characters, and `no description` restores the model's default text.

---

### `system domainname` — changes settings

Assigns a domain name to the system.

**RCI** `/rci/system/domainname`

**Arguments:**

| Argument | Notes |
|---|---|
| `domain` | The domain name to assign. |

**Catch:** NONE

---

### `system eject` — read-only

Stops and ejects a named SCSI/SATA USB drive.

**RCI** `/rci/system/eject`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | The media-drive name to eject. |

**Catch:** ejection is initiated asynchronously: the example reports that eject has started rather than that the drive is already ejected.

---

### `system hostname` — changes settings

Sets the host name used to identify the node.

**RCI** `/rci/system/hostname`

**Arguments:**

| Argument | Notes |
|---|---|
| `hostname` | Host name assigned to the node. |

**Catch:** the `no` form does not clear the name; it restores a default that depends on the device model.

---

### `system led` — changes settings

Binds a general-purpose LED to one of the documented status indicators.

**RCI** `/rci/system/led`

**Arguments:**

| Argument | Notes |
|---|---|
| `led` | Either `FN_1` or `FN_2`. |
| `control` | Selects one of `UpdatesAvailable`, `BackupWan`, `SelectedWan`, `SelectedSchedule`, `OpkgLedControl`, `Usb1PortDeviceAttached`, or `Usb2PortDeviceAttached`. |
| `indicate` | Keyword used by the command to turn the indicator completely off. |

**Catch:** `no led <led> indicate` removes the current binding, whereas bare `no led <led>` restores the LED's default USB-device indication; the two removal forms are not equivalent.

---

### `system led power schedule` — changes settings

Assigns a schedule to the device LEDs.

**RCI** `/rci/system/led/power/schedule`

**Arguments:**

| Argument | Notes |
|---|---|
| `schedule` | The schedule must already have been created and customized with schedule actions. |

**Catch:** a schedule that exists without its schedule actions is not ready for execution.

---

### `system led power shutdown` — changes settings

Selects which device LEDs are shut down.

**RCI** `/rci/system/led/power/shutdown`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | `all`, `front`, or `back`, selecting the LED group to shut down. |

**Catch:** the argument-free `no` form clears the shutdown mode and turns the LEDs back on.

---

### `system log clear` — read-only

Clears the system log.

**RCI** `/rci/system/log/clear`

**Catch:** the operation removes the system log wholesale.

---

### `system log reduction` — changes settings

Controls reduction of repeated log messages.

**RCI** `/rci/system/log/reduction`

**Catch:** NONE

---

### `system log server` — changes settings

Adds a remote log server.

**RCI** `/rci/system/log/server`

**Arguments:**

| Argument | Notes |
|---|---|
| `address` | Address of the remote log server. |
| `port` | Optional remote log server port. |

**Catch:** each invocation adds a remote server, so issuing the command repeatedly builds a set rather than replacing one existing server.

---

### `system log suppress` — changes settings

Adds a rule that suppresses messages from a specified process.

**RCI** `/rci/system/log/suppress`

**Arguments:**

| Argument | Notes |
|---|---|
| `ident` | Process identifier whose messages are suppressed. |

**Catch:** suppression rules accumulate as separate entries; the matching `no` form removes a rule rather than disabling suppression globally.

---

### `system mode` — changes settings

Selects the operating mode for the device.

**RCI** `/rci/system/mode`

**Arguments:**

| Argument | Notes |
|---|---|
| `mode` | One of `router`, `client`, `repeater`, or `ap`; the latter three select the corresponding adapter, wireless repeater, or wired access-point mode. |

**Catch:** the new mode is not active immediately: the example says the device must be rebooted to apply it.

---

### `system mount` — read-only

Mounts a USB filesystem.

**RCI** `/rci/system/mount`

**Arguments:**

| Argument | Notes |
|---|---|
| `filesystem` | The filesystem name used for the mount or unmount operation. |

**Catch:** the no-prefix form unmounts the named filesystem; it is not a reset of the mount configuration.

---

### `system ndss dump-report disable` — changes settings

Disables the product-improvement dump-reporting program.

**RCI** `/rci/system/ndss/dump-report/disable`

**Catch:** NONE

---

### `system reboot` — read-only

Schedules or initiates a system reboot.

**RCI** `/rci/system/reboot`

**Arguments:**

| Argument | Notes |
|---|---|
| `interval` | A timeout in seconds; omitting it from the positive form means immediate reboot. |
| `schedule` | The name of a previously created schedule. |

**Catch:** setting a new interval replaces an existing reboot timer rather than adding another one. The no-prefix form cancels a pending reboot without an argument, while `no reboot schedule` disables the reboot schedule.

---

### `system set` — changes settings

Sets a named system parameter in the current settings.

**RCI** `/rci/system/set`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | Identifier of the system parameter. |
| `value` | New value assigned to that parameter. |

**Catch:** `no set <name>` restores the named parameter's default from before its first change rather than merely deleting the displayed setting.

---

### `system swap` — changes settings

Configures a swap area at a filesystem path.

**RCI** `/rci/system/swap`

**Arguments:**

| Argument | Notes |
|---|---|
| `area` | Full swap-file path in `<file system>:<path>` form. |
| `size` | Swap-file size in kilobytes. |

**Catch:** a missing swap file is created automatically, and initialization runs in the background rather than completing synchronously with the command.

---

### `system trace lock threshold` — read-only

Sets the lock threshold for system threads.

**RCI** `/rci/system/trace/lock/threshold`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | A millisecond value from 100 through 100000000; the value is not saved in startup-config. |

**Catch:** the feature is disabled by default, and the no-prefix form disables it again rather than setting a numeric threshold.

---

### `system usb power schedule` — changes settings

Assigns a power schedule to a USB port.

**RCI** `/rci/system/usb/power/schedule`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | USB port selected for the schedule. |
| `schedule` | The schedule must already have been created and customized with schedule actions. |

**Catch:** the argument table lists only port 2, but the example assigns a schedule to port 1; the block does not say whether both ports are accepted.

---

### `system usb power shutdown` — changes settings

Switches off power to a USB port.

**RCI** `/rci/system/usb/power/shutdown`

**Arguments:**

| Argument | Notes |
|---|---|
| `port` | USB port whose power state is changed. |

**Catch:** the argument table lists only port 2 while the example uses port 1, so the block leaves the accepted port set unresolved; the `no` form restores power.

---

### `system zram` — changes settings

Configures or removes the router's zRam swap file.

**RCI** `/rci/system/zram`

**Arguments:**

| Argument | Notes |
|---|---|
| `size` | zRam size in kilobytes. |

**Catch:** omitting `size` requests automatic sizing rather than disabling zRam; disabling it is a separate `no zram` operation.
