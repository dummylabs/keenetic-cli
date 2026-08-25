# `cloud` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `cloud control2 security-level` — changes settings

Sets the interface security scope through which the Keenetic mobile application's Cloud Control2 service may be accessed.

**RCI** `/rci/cloud/control2/security-level`

**Arguments:**

| Argument | Notes |
|---|---|
| `public` | Allows access from public, private, and protected interfaces. |
| `private` | Allows access from private interfaces only. |

**Catch:** selecting `private` excludes both public and protected interfaces, not merely interfaces classified as public.
