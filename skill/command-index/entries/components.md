# `components` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `components` — read-only

Enters the configuration context for managing firmware components.

**RCI** `/rci/components`

**Catch:** NONE

### `components auto-update channel` — changes settings

Selects the component source channel used for automatic updates.

**RCI** `/rci/components/auto-update/channel`

**Arguments:**

| Argument | Notes |
|---|---|
| `channel` | `stable`, `preview`, or `draft`; the web interface labels these Main, Preview, and Dev respectively. |

**Catch:** the CLI channel names do not match the web interface labels: `stable` is shown as Main and `draft` as Dev.

### `components auto-update disable` — changes settings

Enables or disables automatic component updates.

**RCI** `/rci/components/auto-update/disable`

**Catch:** NONE

### `components auto-update schedule` — changes settings

Associates a previously defined schedule with component automatic updates.

**RCI** `/rci/components/auto-update/schedule`

**Arguments:**

| Argument | Notes |
|---|---|
| `schedule` | Name of a schedule created through the schedule command group. |

**Catch:** the schedule must already have been created and customized with a schedule action before it can be used here.

### `components check-update` — read-only

Checks for firmware updates for a Modular Wi-Fi System candidate or member.

**RCI** `/rci/components/check-update`

**Arguments:**

| Argument | Notes |
|---|---|
| `force` | Requests constant checking for updates. |

**Catch:** NONE

**Returns (report labels):** `release`, `sandbox`, `timestamp`, `valid`.

### `components commit` — changes settings

Applies component installation and removal operations that have been staged.

**RCI** `/rci/components/commit`

**Catch:** `components install` and `components remove` only queue changes; those changes are not applied until this command is executed.

### `components install` — changes settings

Queues a component for installation.

**RCI** `/rci/components/install`

**Arguments:**

| Argument | Notes |
|---|---|
| `component` | Component name; available installation choices are listed by `components list`. |

**Catch:** this command only marks the component; the installation occurs when `components commit` is run.

### `components list` — read-only

Switches to a selected sandbox and queues components whose versions need to change, or lists the current sandbox's components.

**RCI** `/rci/components/list`

**Arguments:**

| Argument | Notes |
|---|---|
| `sandbox` | Remote sandbox name, such as `stable` or `beta`. |

**Catch:** specifying a sandbox can mark components for installation rather than merely selecting a view, and without Internet access the list contains only installed components; the example also shows repeated `preset` keys, so a parser must preserve all preset values.

**Returns (fields):** `firmware`, `version`, `sandbox`, `local`, `component`, `name`, `priority`, `size`, `hash`, `installed`, `preset`, `queued`.

### `components preset` — changes settings

Stages a predefined component set for installation.

**RCI** `/rci/components/preset`

**Arguments:**

| Argument | Notes |
|---|---|
| `preset` | The documented choices are `minimal` and `recommended`; the available set can change and is exposed by CLI completion. |

**Catch:** choosing a preset marks components rather than installing them immediately, and the block requires an internet connection and an up-to-date component list before installation.

### `components preview` — changes settings

Reports the firmware size implied by the currently selected component set.

**RCI** `/rci/components/preview`

**Catch:** NONE

**Returns (fields):** `preview`, `size`.

### `components remove` — changes settings

Queues a component for removal.

**RCI** `/rci/components/remove`

**Arguments:**

| Argument | Notes |
|---|---|
| `component` | Component name; available removal choices are listed by `components list`. |

**Catch:** this command only marks the component; the removal occurs when `components commit` is run.

### `components validity-period` — changes settings

Sets how long the locally cached component list remains valid.

**RCI** `/rci/components/validity-period`

**Arguments:**

| Argument | Notes |
|---|---|
| `seconds` | Cache-validity interval, accepted from 0 through 604800 seconds. |

**Catch:** after the interval expires, `components list` is automatically run to fetch the current list from the update server; omitting the setting resets it to 1800 seconds.
