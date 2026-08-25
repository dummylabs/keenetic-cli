# `sms` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `sms` — read-only

Enters the SMS command context for a selected USB interface.

**RCI** `/rci/sms`

**Arguments:**

| Argument | Notes |
|---|---|
| `name` | The USB interface that supplies the SMS service. |

**Catch:** NONE

---

### `sms delete` — read-only

Deletes an SMS message by identifier.

**RCI** `/rci/sms/delete`

**Arguments:**

| Argument | Notes |
|---|---|
| `id` | The message identifier. |

**Catch:** NONE

---

### `sms list` — read-only

Lists received SMS messages, optionally filtering them or suppressing their text.

**RCI** `/rci/sms/list`

**Arguments:**

| Argument | Notes |
|---|---|
| `unread` | Limits the result to unread messages. |
| `id` | Selects the message with the specified identifier. |
| `no-content` | Suppresses message text in the result. |

**Catch:** the output is not uniform across the examples: a multipart message can report fewer received `parts` than `total-parts`, and the `no-content` form shows records with `read` but no message text (the block does not promise which other fields are omitted). Storage totals are also split between `nv` and `sim` slots.

**Returns (fields):** `nv-free-slots`, `nv-total-slots`, `sim-free-slots`, `sim-total-slots`, `messages-count`, `messages`, `id`, `read`, `from`, `timestamp`, `parts`, `total-parts`, `text`.

---

### `sms read` — read-only

Marks the identified SMS as read.

**RCI** `/rci/sms/read`

**Arguments:**

| Argument | Notes |
|---|---|
| `id` | The message identifier. |

**Catch:** the no-prefix form reverses the operation and marks the message unread.

---

### `sms send` — read-only

Sends a text message to a specified telephone number.

**RCI** `/rci/sms/send`

**Arguments:**

| Argument | Notes |
|---|---|
| `to` | The recipient's telephone number. |
| `message` | The text to send. |

**Catch:** incoming SMS storage is capped at 128 messages; when it is full, receiving a new message automatically removes the oldest stored message.

---
