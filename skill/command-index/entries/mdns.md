# `mdns` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `mdns` — read-only

Enters the command group for managing the mDNS service.

**RCI** `/rci/mdns`

**Catch:** NONE

### `mdns reflector disable` — changes settings

Forces mDNS transparency between home-network segments off.

**RCI** `/rci/mdns/reflector/disable`

**Catch:** this setting takes precedence over segment-isolation status, so changing an interface security level does not by itself override it.

### `mdns reflector enforce` — changes settings

Forces mDNS transparency between home-network segments on.

**RCI** `/rci/mdns/reflector/enforce`

**Catch:** this setting also bypasses segment-isolation status, so transparency is forced even when the segments would otherwise be isolated.
