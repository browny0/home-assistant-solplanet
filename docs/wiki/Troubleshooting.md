# Troubleshooting

## Integration Cannot Connect

1. Confirm the dongle is powered and still appears in your router's connected-device list.
2. Enter only its IP address or hostname in Home Assistant, without a protocol or port.
3. Confirm Home Assistant can reach TCP port 443 or 8484 on the dongle. Ping is not required.
4. Check firewall rules, guest Wi-Fi isolation, and VLAN routing.
5. Confirm only one Solplanet custom integration is installed.
6. If you moved from the original integration, remove its HACS repository before reinstalling this one.
7. Run the tests in [Advanced Local Access](Advanced-Local-Access#test-the-connection).

A failed HTTPS test does not mean the dongle is unsupported. It may use HTTP on port 8484 instead.

## Dongle Address Or Wi-Fi Is Missing

- Check your router's DHCP client list and create a reservation when you find the dongle.
- Stand close to the dongle if you are looking for its temporary Wi-Fi access point.
- Open the Solplanet app's **Configure Parameters** flow and load a saved QR-code photo if the physical label is difficult to scan.
- Check the app's dongle details for the current IP address.

Some dongles hide their access point after joining your home Wi-Fi. This does not prevent local access through the home network.

## Data Is Slow Or Occasionally Missing

The default update interval is 60 seconds. Each update reads several endpoints in sequence, so a busy or slow dongle can take longer than the configured interval.

- Keep the default interval while diagnosing the problem.
- Remove duplicate REST sensors or other software polling the dongle.
- On V2 systems, check **WiFi signal strength** and improve coverage if the signal is weak.
- Check the dongle **Warnings** entity.
- If the **Reboot** button is available, restart the dongle only after allowing a normal update to finish.
- Review **Settings > System > Logs** and search for `solplanet`.

An individual value may show `unknown` while an inverter or battery is sleeping. If the integration cannot complete an update, its entities become unavailable until communication recovers.

## An Action Fails

For battery schedule actions, target the battery's **Schedule Configured** binary sensor.

For power-limit actions, use the **Meter device** field and select the main meter. The action will reject an inverter, battery, or dongle. Do not select a sub-meter because it is not an independent control target and may send the same system-wide setting. Power-limit actions also require a supported V2 system.

## Meter Values Look Wrong

- Compare **Meter power**, or **Grid power** on a V1 system, with the Solplanet app while turning a known appliance on and off.
- Confirm whether your installation treats positive power as import or export before building automations.
- Check for a reversed or incorrectly positioned CT clamp.
- Check whether controlled loads sit inside or outside the meter's measurement point.
- Confirm the integration is using the main meter you expect.
- Remember that V2 sub-meters can appear as devices without live entities.

We do not expose a native house-load sensor. If a calculated house-load value looks wrong, the calculation may not match your system topology or its source entities may have updated at different times.

Meter and CT issues should be checked by a qualified electrician or installer.

## Battery Will Not Charge Or Discharge Fully

- Check **Work mode**, **SOC min**, **SOC max**, and any active schedule.
- Check whether **Power limit control** is active on the meter.
- Review battery **Communication status**, **Battery errors**, and **Battery warnings**.
- Confirm all battery stacks show consistent status lights and are contributing power.
- Check whether the reported charge or discharge current limit is unexpectedly low.
- Ask your installer to check DC cables, combiner-box connections, and RJ45 communication cables.

Stack, cable, or combiner-box faults can reduce the available current without being caused by Home Assistant.

## W177 Battery Communication Error

W177 can be expected while the battery is intentionally powered off. It should clear after the battery is powered on and the inverter detects it again. If it remains, check the communication status and contact your installer.

## Flashing Yellow Battery Light

A flashing yellow light commonly indicates lost battery communication. Check the Home Assistant communication and warning entities, then ask your installer to inspect RJ45 connectors and stack interconnects if the warning persists.

## Power Limit Control Stops Charging

- Run **Disable power limit control** against the main meter before the charging window.
- If disabling fails while using absolute **Limit power**, set **Export power limit setpoint (W)** to 0 without changing the other required fields, then try disabling it again. This workaround does not apply to **Limit current** or **Zero power**.
- If available, check that the meter's **Power limit control** diagnostic entity reads **Disabled**.
- Limit automations to the required export window and always add a disable action at the end.
- Re-test after firmware or Solplanet-side changes.

This behaviour varies by inverter and firmware.

## Firmware And Remote Changes

Our integration does not install inverter, battery, or dongle firmware. Depending on your account, the Solplanet app may offer a battery update; inverter updates are normally managed by Solplanet or an installer.

After any firmware or remote configuration change, re-check charging, discharging, work modes, schedules, Power Limit Control, and meter values before relying on your automations again.
