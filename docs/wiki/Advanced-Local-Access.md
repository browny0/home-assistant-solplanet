# Advanced Local Access

Our integration communicates directly with the inverter dongle. Normal setup does not require any endpoint commands, certificates, serial numbers, or cloud credentials. This page is for advanced troubleshooting and users who want to run the dongle without internet access.

## How We Connect

During setup, we try these local connection methods automatically:

1. V2 over HTTPS on port 443.
2. V2 over HTTP on port 8484.
3. V1 over HTTP on port 8484.

HTTPS dongles use a self-signed certificate, so the integration disables certificate verification for this local connection. Enter only the IP address or hostname during setup; we add the protocol and port.

## Test The Connection

Run these commands from a machine that has the same network access as Home Assistant. Replace `<host>` with the dongle IP address or hostname.

```bash
curl -k "https://<host>/getdev.cgi?device=2"
curl "http://<host>:8484/getdev.cgi?device=2"
curl "http://<host>:8484/invinfo.cgi"
```

You do not need all three commands to work. A JSON or device-data response from one of them identifies a usable local API. If every command times out or refuses the connection, check the address, VLAN rules, Wi-Fi client isolation, and ports 443 and 8484.

## Run Without Cloud Access

You can use the local integration while blocking the dongle from the internet, provided Home Assistant can still reach it. This may remove Solplanet app history, remote access, firmware delivery, or installer support, depending on your system.

The dongle clock can drift without its normal time source. On V2 systems, use the dongle's **Sync time** button in Home Assistant when needed, or call it from an automation. Blocking cloud access does not necessarily improve polling speed or reliability because the dongle may continue attempting outbound connections.

## Protect Local Access

The integration does not ask for a dongle username or password. Anyone who can reach the same local endpoints may also be able to read data or change settings.

- Keep the dongle on a trusted network or isolated IoT VLAN.
- Allow access only from Home Assistant and other trusted administration devices where practical.
- Do not expose ports 443 or 8484 to the internet.
- Do not share the dongle QR code or password label.

## Avoid Overloading The Dongle

The dongle has limited processing capacity. Fast polling or requests from multiple clients can cause timeouts and make both Home Assistant and the Solplanet app slow. The integration serializes its own reads and writes so they do not overlap, but REST sensors, scripts, the app, and other software do not share that protection.

- Use the integration instead of duplicating its requests with REST sensors.
- Keep the default 60-second live data interval unless you have a clear need to change it.
- Stagger any additional requests rather than sending them together.
- Expect different groups of entities to update at slightly different times while their requests wait for the dongle.

The configurable interval applies to live inverter, battery, meter, and dongle-warning data. Inventory and settings use a separate hourly refresh. After three consecutive full failures, the affected live-data poller waits at least 10 minutes between attempts and returns to the configured interval after communication recovers.

## Raw Endpoints And Modbus

For V2 hardware, the integration uses local CGI endpoints to read device data and apply supported settings. It also uses `fdbg.cgi` to tunnel some Modbus reads and writes. Responses can contain raw hexadecimal Modbus data rather than user-friendly values.

Do not send write payloads copied from a forum post or another inverter model. A raw write can change battery operation, inverter power, export compliance settings, or other safety-related configuration. Use the entities and actions we provide, where inputs can be validated, instead of calling raw control endpoints.
