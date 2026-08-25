# `user` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `user` — changes settings

Opens the command group for configuring a user account.

**RCI** `/rci/user`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | User name; an unknown name is treated as a request to create the account. |

**Catch:** the reserved `admin` account cannot be removed and cannot lose command-line access.

---

### `user home` — changes settings

Sets the user's home directory.

**RCI** `/rci/user/home`

**Arguments:**

| Argument | Notes |
|---|---|
| `directory` | Filesystem path used as the home directory. |

**Catch:** the same configured directory is used by the user's FTP, SFTP, and WebDAV services.

---

### `user password generate` — changes settings

Generates a random password for the current user account without saving it.

**RCI** `/rci/user/password/generate`

**Catch:** the generated value is not saved, but it is emitted in the command output and should be treated as a secret.

**Returns (fields):** `password`

---

### `user password md5` — changes settings

Sets the user's MD5 password hash.

**RCI** `/rci/user/password/md5`

**Arguments:**

| Argument | Notes |
|---|---|
| `hash` | MD5 hash value supplied for the account. |

**Catch:** NONE

---

### `user password nt` — changes settings

Sets the user's NT password hash.

**RCI** `/rci/user/password/nt`

**Arguments:**

| Argument | Notes |
|---|---|
| `hash` | NT hash value supplied for the account. |

**Catch:** NONE

---

### `user password plain` — changes settings

Sets the user's plain-text password.

**RCI** `/rci/user/password/plain`

**Arguments:**

| Argument | Notes |
|---|---|
| `password` | Between 8 and 64 characters; the block recommends mixing letter cases, digits, and special characters. |

**Catch:** the command takes the password in plain text, so the credential is present directly in the command invocation.

### `user password validate` — read-only

Assesses a supplied password against the documented length and compliance checks.

**RCI** `/rci/user/password/validate`

**Arguments:**

| Argument | Notes |
|---|---|
| `value` | The password must be at least 8 characters; 15 characters is the stated recommendation. |

**Catch:** the example does not use one fixed report shape: one result contains only a strength assessment, while another also prints length guidance. The length section is therefore an observed conditional output, not a guaranteed part of every response.

**Returns (report labels):** `strength`, `length`, `required`, `recommended`.

### `user tag` — changes settings

Assigns or removes permission tags on a user account.

**RCI** `/rci/user/tag`

**Arguments:**

| Argument | Notes |
|---|---|
| `tag` | One of the documented access tags, including `cli`, `manager`, `readonly`, `http-proxy`, `http`, `afp`, `printers`, `cifs`, `vpn-dlna`, `ftp`, `ipsec-xauth`, `ipsec-l2tp`, `vpn-oc`, `opt`, `sftp`, `sstp`, `torrent`, `vpn`, and `webdav`. |

**Catch:** tags accumulate across repeated calls rather than replacing one another, and the admin account cannot have `cli` removed; its `http` tag also cannot be removed when the device is an MWS Extender.

**Blast radius:** bare `no tag` clears every tag on the current user account.
