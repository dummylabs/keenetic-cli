# `ip` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `ip ssh` — read-only

Enters the command group for managing the SSH server.

**RCI** `/rci/ip/ssh`

**Catch:** NONE

### `ip ssh cipher` — changes settings

Adds an allowed symmetric cipher for SSH sessions.

**RCI** `/rci/ip/ssh/cipher`

**Arguments:**

| Argument | Notes |
|---|---|
| `cipher` | One of `chacha20-poly1305@openssh.com`, `aes128-ctr`, `aes256-ctr`, `aes128-gcm@openssh.com`, or `aes256-gcm@openssh.com`. |

**Catch:** cipher invocations add individual algorithms rather than selecting one replacement value; in the one-entry example, removing that entry causes the router to report that it is using the default ciphers.

### `ip ssh keygen` — changes settings

Regenerates SSH keys of the requested type.

**RCI** `/rci/ip/ssh/keygen`

**Arguments:**

| Argument | Notes |
|---|---|
| `keygen` | Accepted values are `default`, `rsa-1024`, `rsa-2048`, `rsa-4096`, `ecdsa-nistp256`, `ecdsa-nistp384`, `ecdsa-nistp521`, and `ed25519`; `default` generates RSA2048 and ECDSA-NISTP521 keys together. |

**Catch:** key generation is asynchronous: the example returns “in progress” status rather than waiting for the new key material to be ready.

### `ip ssh lockout-policy` — changes settings

Configures SSH brute-force detection thresholds and timing for public interfaces.

**RCI** `/rci/ip/ssh/lockout-policy`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | Failed-login threshold from 4 to 20; the documented default is 5. |
| `duration` | Ban duration from 1 to 60 minutes; the documented default is 15. |
| `observation-window` | Suspicious-activity window from 1 to 10 minutes; the documented default is 3. |

**Catch:** a threshold of `0` is a reset-to-default sentinel for all detection parameters, while the no-form disables detection altogether.

### `ip ssh port` — changes settings

Sets the SSH connection port, defaulting to 22.

**RCI** `/rci/ip/ssh/port`

**Arguments:**

| Argument | Notes |
|---|---|
| `number` | Port number from 1 through 65535; the no-form restores 22. |

**Catch:** NONE

### `ip ssh security-level` — changes settings

Selects the interface security levels permitted to access the SSH server.

**RCI** `/rci/ip/ssh/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Permits access from public, private, and protected interfaces. |
| `private` | Permits access from private interfaces only. |
| `protected` | Permits access from private and protected interfaces. |

**Catch:** NONE

### `ip ssh session timeout` — changes settings

Sets the lifetime of an inactive SSH session.

**RCI** `/rci/ip/ssh/session/timeout`

**Arguments:**

| Argument | Notes |
|---|---|
| `timeout` | Inactivity lifetime from 5 through 2^32−1 seconds; the documented default is 300 seconds. |

**Catch:** the default value of 300 seconds is described as disabling activity tracking, so the default does not behave like an ordinary active inactivity timeout; the no-form restores that default.

### `ip ssh sftp` — read-only

Enters the command group for managing the SFTP server.

**RCI** `/rci/ip/ssh/sftp`

**Catch:** NONE

### `ip ssh sftp enable` — changes settings

Enables the SFTP server.

**RCI** `/rci/ip/ssh/sftp/enable`

**Catch:** NONE

### `ip ssh sftp permissive` — changes settings

Controls unrestricted SFTP access.

**RCI** `/rci/ip/ssh/sftp/permissive`

**Catch:** when enabled, all users can access the SFTP server without authentication.

### `ip ssh sftp root` — changes settings

Sets the SFTP server's default root directory.

**RCI** `/rci/ip/ssh/sftp/root`

**Arguments:**

| Argument | Notes |
|---|---|
| `directory` | Path used as the default SFTP root. |

**Catch:** the synopsis defines reset as `no root` with no directory, but the example shows `no root files_ssd:/`; the block is inconsistent about whether the old directory may be supplied on reset.
