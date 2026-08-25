# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface encryption anonymous-dh` — changes settings

Enables anonymous Diffie–Hellman TLS for an SSTP server.

**RCI** `/rci/interface/encryption/anonymous-dh`

**Catch:** This is specifically the certificate-less SSTP-server mode, not a general wireless-encryption option.

### `interface encryption enable` — changes settings

Turns wireless-interface encryption on or off.

**RCI** `/rci/interface/encryption/enable`

**Catch:** NONE

### `interface encryption key` — changes settings

Adds or removes a WEP key and can mark one of the keys as the default.

**RCI** `/rci/interface/encryption/key`

**Arguments:**

| Argument | Notes |
|---|---|
| `id` | Key number; at most four keys can be defined. |
| `value` | Hexadecimal key material of 10 or 26 digits. |
| `default` | Keyword that marks the supplied key as the one used by default. |

**Catch:** A WEP configuration may contain one to four keys, but one of them must be designated as the default; removing or adding keys is therefore not independent of the default-key choice.

### `interface encryption mppe` — changes settings

Enables MPPE encryption support on a PPTP interface.

**RCI** `/rci/interface/encryption/mppe`

**Catch:** NONE

### `interface encryption owe` — changes settings

Enables OWE security algorithms on a wireless interface.

**RCI** `/rci/interface/encryption/owe`

**Catch:** NONE

### `interface encryption tkip hold-down` — changes settings

Sets the TKIP countermeasure interval used with WPA and WPA2.

**RCI** `/rci/interface/encryption/tkip/hold-down`

**Arguments:**

| Argument | Notes |
|---|---|
| `hold-down` | Seconds from 0 through 60; `0` disables the setting. |

**Catch:** `0` is a disable sentinel rather than a zero-second waiting period, while `no encryption tkip hold-down` restores the default interval of 60 seconds.

### `interface encryption wpa` — changes settings

Enables WPA security algorithms on a wireless interface.

**RCI** `/rci/interface/encryption/wpa`

**Catch:** WPA can coexist with WPA2, but enabling either WPA family option automatically turns off WEP support.

### `interface encryption wpa2` — changes settings

Enables WPA2/RSN security algorithms on a wireless interface.

**RCI** `/rci/interface/encryption/wpa2`

**Catch:** WPA2 can coexist with WPA, but enabling either WPA family option automatically turns off WEP support.

### `interface encryption wpa3` — changes settings

Enables WPA3 security algorithms on a wireless interface.

**RCI** `/rci/interface/encryption/wpa3`

**Catch:** WPA3 is designed here to operate jointly with WPA2, and the block says the feature starts disabled.

### `interface encryption wpa3 suite-b` — changes settings

Enables WPA3 Suite-B algorithms for WPA Enterprise.

**RCI** `/rci/interface/encryption/wpa3/suite-b`

**Catch:** There is no `no` form for this command, so the block provides no command-level removal operation despite the feature being disabled by default.
