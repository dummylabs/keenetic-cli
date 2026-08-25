# `easyconfig` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `easyconfig check` — read-only

Enters the command group for configuring Internet-access checks.

**RCI** `/rci/easyconfig/check`

**Catch:** The check sequence tests the default gateway first and only then polls configured remote hosts; Internet access is granted only after all checks succeed.
