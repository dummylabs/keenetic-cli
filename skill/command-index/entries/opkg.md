# `opkg` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `opkg chroot` — changes settings

Enables chroot execution for opkg scripts.

**RCI** `/rci/opkg/chroot`

**Catch:** with chroot enabled, each opkg script runs after its root directory is changed to `/opt`, so scripts do not execute against the ordinary root directory.

### `opkg disk` — changes settings

Selects the partition used as `/opt` for opkg software.

**RCI** `/rci/opkg/disk`

**Arguments:**

| Argument | Notes |
|---|---|
| `disk` | Partition label or UUID. |
| `url` | URL of the installer package. |

**Catch:** configuring the disk immediately bind-mounts it at `/opt`; installation archives found in `/opt/install` are unpacked into `/opt` before initrc runs, so this is an activation step rather than merely a stored partition choice.

**Destructive:** any `.ipk` and `.tgz` archives found in `/opt/install` are unpacked into `/opt` and then deleted; the block does not state whether those archives can be recovered.

### `opkg dns-override` — changes settings

Disables TCP and UDP port 53 for the embedded DNS proxy.

**RCI** `/rci/opkg/dns-override`

**Catch:** enabling this does not select another DNS daemon; it frees port 53 so a custom opkg service such as BIND or Dnsmasq can replace the embedded proxy.

### `opkg initrc` — changes settings

Sets the initial script or script directory used by opkg.

**RCI** `/rci/opkg/initrc`

**Arguments:**

| Argument | Notes |
|---|---|
| `path` | Initial-script file or directory; the documented default is `/opt/etc/initrc`. |

**Catch:** when `path` is a directory, every contained script is executed in alphabetic order after the opkg disk is mounted and packages are installed, rather than the directory itself being run as one script.

### `opkg object-group fqdn enable` — changes settings

Enables FQDN resolution for a named opkg object group.

**RCI** `/rci/opkg/object-group/fqdn/enable`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | FQDN object-group name. |

**Catch:** NONE

### `opkg timezone` — changes settings

Configures the timezone used by opkg software.

**RCI** `/rci/opkg/timezone`

**Arguments:**

| Argument | Notes |
|---|---|
| `timezone` | POSIX timezone specification or a zoneinfo-binary-format timezone filename, written to `/opt/var/TZ` and assigned to `TZ`. |
| `auto` | Generates the timezone specification from the system-wide settings. |

**Catch:** this setting targets opkg's `TZ` environment and `/opt/var/TZ`, not the router's general timezone setting; `auto` derives its value from that separate system-wide configuration.
