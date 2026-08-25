# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface authentication chap` — changes settings

Enables CHAP as an authentication method.

**RCI** `/rci/interface/authentication/chap`

**Catch:** NONE

### `interface authentication eap-md5` — changes settings

Enables EAP-MD5 authentication.

**RCI** `/rci/interface/authentication/eap-md5`

**Catch:** NONE

### `interface authentication eap-mschapv2` — changes settings

Enables EAP-MSCHAPv2 authentication support.

**RCI** `/rci/interface/authentication/eap-mschapv2`

**Catch:** the `no` form removes both EAP-MSCHAPv2 and MS-CHAPv2 authentication, rather than just one independently named method; the example also shows an enable attempt reported as unchanged on IKE0.

### `interface authentication eap-ttls` — changes settings

Enables EAP-TTLS authentication.

**RCI** `/rci/interface/authentication/eap-ttls`

**Catch:** NONE

### `interface authentication identity` — changes settings

Stores the username used when the interface authenticates to a remote system.

**RCI** `/rci/interface/authentication/identity`

**Arguments:**

| Argument | Notes |
|---|---|
| `identity` | The username supplied to the remote authentication system. |

**Catch:** NONE

### `interface authentication mschap` — changes settings

Enables MS-CHAP authentication.

**RCI** `/rci/interface/authentication/mschap`

**Catch:** NONE

### `interface authentication mschap-v2` — changes settings

Enables MS-CHAPv2 authentication.

**RCI** `/rci/interface/authentication/mschap-v2`

**Catch:** the example shows an enable attempt on PPTP0 being reported as unchanged; the block does not state when that result occurs.

### `interface authentication pap` — changes settings

Enables PAP authentication.

**RCI** `/rci/interface/authentication/pap`

**Catch:** NONE

### `interface authentication password` — changes settings

Stores the password used for remote authentication.

**RCI** `/rci/interface/authentication/password`

**Arguments:**

| Argument | Notes |
|---|---|
| `password` | The credential used by the interface for remote authentication. |

**Catch:** the example does not echo the supplied password when saving or clearing it.

### `interface authentication peap` — changes settings

Enables EAP-PEAP authentication.

**RCI** `/rci/interface/authentication/peap`

**Catch:** NONE

### `interface authentication shared` — changes settings

Selects shared-key authentication for the wireless interface.

**RCI** `/rci/interface/authentication/shared`

**Catch:** this mode is usable only together with WEP encryption; the `no` form switches authentication back to open mode rather than merely removing a method.

### `interface authentication wpa-psk` — changes settings

Sets the pre-shared credential used by WPA-PSK authentication.

**RCI** `/rci/interface/authentication/wpa-psk`

**Arguments:**

| Argument | Notes |
|---|---|
| `psk` | Accepts either 64 hexadecimal digits or an ASCII passphrase from 8 through 63 characters. |

**Catch:** the supplied key is not printed in the command's confirmation output.
