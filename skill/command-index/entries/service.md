# `service` commands

Derived from the Keenetic KN-1011 CLI manual (OS 5.0). Wording is original; nothing here has been run against a router.

### `service afp` — changes settings

Enables the AFP service.

**RCI** `/rci/service/afp`

**Catch:** NONE

### `service cifs` — changes settings

Enables the CIFS service.

**RCI** `/rci/service/cifs`

**Catch:** NONE

### `service dhcp` — changes settings

Enables the DHCP server.

**RCI** `/rci/service/dhcp`

**Catch:** The server will not answer on the network until the related DHCP-pool settings are sufficient, after which it enables automatically.

### `service dhcp-relay` — changes settings

Enables DHCP relay service.

**RCI** `/rci/service/dhcp-relay`

**Catch:** Relay traffic remains unanswered until LAN, server, and WAN relay settings are sufficient, after which the service enables automatically.

### `service dlna` — changes settings

Enables the DLNA service.

**RCI** `/rci/service/dlna`

**Catch:** The service will not respond on the network until its related DLNA settings are sufficient, after which it enables automatically.

### `service dns-proxy` — changes settings

Enables the DNS proxy service.

**RCI** `/rci/service/dns-proxy`

**Catch:** Service parameters are configured through the separate DNS-proxy command group rather than this switch.

### `service ftp` — changes settings

Enables the FTP server for access to attached storage and selected device files.

**RCI** `/rci/service/ftp`

**Catch:** Enabling FTP exposes connected USB-drive contents, configuration files, and the firmware-update file through that service.

### `service http` — changes settings

Enables the HTTP server that provides the device's Web configuration interface.

**RCI** `/rci/service/http`

**Catch:** This service exposes the Web interface used to configure the device, rather than only a generic HTTP endpoint.

### `service igmp-proxy` — changes settings

Enables the IGMP proxy service.

**RCI** `/rci/service/igmp-proxy`

**Catch:** The proxy requires one upstream interface and at least one downstream interface; it starts automatically once those prerequisites are present.

### `service internet-checker` — changes settings

Enables the Internet-checker service.

**RCI** `/rci/service/internet-checker`

**Catch:** The service is enabled by default, and the argument-free `no` form disables the host checks.

### `service ipsec` — changes settings

Enables the IPsec service.

**RCI** `/rci/service/ipsec`

**Catch:** The service is disabled by default, so its initial state is off until explicitly enabled.

### `service kabinet` — changes settings

Controls the КАБiNET authenticator service.

**RCI** `/rci/service/kabinet`

**Catch:** The example shows two consecutive positive invocations changing the authenticator from enabled to disabled, so the positive form appears to toggle rather than simply enable; the block does not explain that behavior.

### `service mdns` — changes settings

Enables the mDNS service.

**RCI** `/rci/service/mdns`

**Catch:** The service is enabled by default, so the positive command is not required to make its initial state active.

### `service mws` — changes settings

Enables the MWS service.

**RCI** `/rci/service/mws`

**Catch:** NONE

### `service ntce` — changes settings

Enables the NTCE service.

**RCI** `/rci/service/ntce`

**Catch:** The history identifies `service dpi` as the previous command name, which matters when translating older configuration or automation.

### `service ntp` — changes settings

Enables the NTP service.

**RCI** `/rci/service/ntp`

**Catch:** The service is enabled by default, and the history identifies `service ntp-client` as its previous command name.

### `service oc-server` — changes settings

Enables the OpenConnect server.

**RCI** `/rci/service/oc-server`

**Catch:** NONE

### `service snmp` — changes settings

Enables the SNMP service.

**RCI** `/rci/service/snmp`

**Catch:** The service is disabled by default, so enabling it changes an initially inactive service.

### `service ssh` — changes settings

Enables the SSH server for the device's command-line configuration interface.

**RCI** `/rci/service/ssh`

**Catch:** Enabling this service exposes a command-line interface for configuring the device.

### `service sstp-server` — changes settings

Enables the SSTP server.

**RCI** `/rci/service/sstp-server`

**Catch:** NONE

### `service telnet` — changes settings

Enables the Telnet server for the device's command-line configuration interface.

**RCI** `/rci/service/telnet`

**Catch:** The example invokes `service tel` while the synopsis documents `service telnet`; the block does not clarify whether the shortened form is accepted or is an extraction error.

### `service torrent` — changes settings

Enables the BitTorrent client.

**RCI** `/rci/service/torrent`

**Catch:** Enabling this service activates peer-to-peer sharing of large files, as described for the client.

### `service udpxy` — changes settings

Enables the udpxy service.

**RCI** `/rci/service/udpxy`

**Catch:** NONE

### `service upnp` — changes settings

Enables the UPnP service.

**RCI** `/rci/service/upnp`

**Catch:** NONE

### `service vpn-server` — changes settings

Enables the VPN server.

**RCI** `/rci/service/vpn-server`

**Catch:** NONE
