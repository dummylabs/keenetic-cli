# `interface` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `interface traffic-counter action disconnect` — changes settings

Configures the USB traffic counter to disconnect its provider when the traffic limit trigger fires.

**RCI** `/rci/interface/traffic-counter/action/disconnect`

**Arguments:**

| Argument | Notes |
|---|---|
| `trigger` | The documented trigger is `limit`. |

**Catch:** NONE

### `interface traffic-counter action sms-alert message` — changes settings

Stores the SMS text used by a USB traffic-counter alert action.

**RCI** `/rci/interface/traffic-counter/action/sms-alert/message`

**Arguments:**

| Argument | Notes |
|---|---|
| `trigger` | Selects either the `threshold` alert or the `limit` alert. |
| `message` | Text sent for the selected alert. |

**Catch:** NONE

### `interface traffic-counter action sms-alert phone` — changes settings

Adds a destination phone number to a USB traffic-counter SMS alert.

**RCI** `/rci/interface/traffic-counter/action/sms-alert/phone`

**Arguments:**

| Argument | Notes |
|---|---|
| `trigger` | Selects either the `threshold` alert or the `limit` alert. |
| `phone` | A destination number; no more than three numbers can be set. |

**Catch:** Phone numbers are added to the selected alert action rather than replacing its existing numbers, so repeated calls consume the three-number allowance.

### `interface traffic-counter enable` — changes settings

Turns the USB mobile traffic counter on or off.

**RCI** `/rci/interface/traffic-counter/enable`

**Catch:** NONE

### `interface traffic-counter limit` — changes settings

Sets the USB traffic counter's limit and its unit.

**RCI** `/rci/interface/traffic-counter/limit`

**Arguments:**

| Argument | Notes |
|---|---|
| `value` | The numeric limit. |
| `unit` | One of `MB`, `GB`, `TB`, `MiB`, `GiB`, or `TiB`. |

**Catch:** NONE

### `interface traffic-counter monthly` — changes settings

Chooses the calendar day on which the USB traffic counter restarts.

**RCI** `/rci/interface/traffic-counter/monthly`

**Arguments:**

| Argument | Notes |
|---|---|
| `day-of-month` | A day from `1` through `31`. |

**Catch:** NONE

### `interface traffic-counter set` — changes settings

Sets the current USB traffic-counter reading to a supplied amount and unit.

**RCI** `/rci/interface/traffic-counter/set`

**Arguments:**

| Argument | Notes |
|---|---|
| `value` | The counter accepts a fractional numeric value as well as a whole number. |
| `unit` | One of `MB`, `GB`, `TB`, `MiB`, `GiB`, or `TiB`. |

**Catch:** The argument table labels `value` as an integer even though the documented input may be floating point, so callers must not reject decimal readings.

### `interface traffic-counter threshold` — changes settings

Sets the percentage of the USB traffic limit at which a warning is triggered.

**RCI** `/rci/interface/traffic-counter/threshold`

**Arguments:**

| Argument | Notes |
|---|---|
| `threshold` | A percentage from `1` through `99` of the configured limit. |

**Catch:** NONE
