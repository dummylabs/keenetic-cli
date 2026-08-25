# `torrent` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `torrent` — read-only

Provides the CLI context for BitTorrent-related operations.

**RCI** `/rci/torrent`

**Catch:** NONE

### `torrent reset` — read-only

Restores the BitTorrent client's settings through a single reset action.

**RCI** `/rci/torrent/reset`

**Catch:** NONE

**Returns (report labels):** `Torrent::Client`, `Reset performed`.
