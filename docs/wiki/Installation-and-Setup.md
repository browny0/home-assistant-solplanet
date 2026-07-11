# Installation and Setup

## Before You Start

You need:

- Home Assistant 2026.3.0 or newer.
- A Solplanet inverter with a network-connected smart dongle.
- The IP address or hostname of the dongle.
- Network access from Home Assistant to the dongle.

You do not need your inverter serial number, a Solplanet cloud account, or installer credentials.

## Install With HACS

1. Open HACS.
2. Select the three-dot menu, then **Custom repositories**.
3. Add `https://github.com/calvinbui/home-assistant-solplanet` as an **Integration** repository.
4. Find and install **Solplanet**.
5. Restart Home Assistant when HACS asks you to.

If you are moving from another Solplanet custom integration, remove the old repository and integration first. Keeping both variants installed can cause HACS or Home Assistant to load the wrong files.

## Install Manually

1. Copy `custom_components/solplanet` from this repository to `config/custom_components/solplanet` in your Home Assistant configuration directory.
2. Restart Home Assistant.

## Add Your System

1. Open **Settings > Devices & services**.
2. Select **Add integration**.
3. Search for **Solplanet**.
4. Enter the dongle IP address or hostname without `http://`, `https://`, or a port number.
5. Leave the update interval at 60 seconds for your first setup.
6. Submit the form and wait for the first update to finish.

We automatically try the supported HTTPS and HTTP connection methods. When setup succeeds, we create devices for the inverter and any batteries, meters, or dongles that the system reports.

After setup, open the new Solplanet devices and confirm that power and state-of-charge values update. Some values from sleeping hardware may show `unknown`; see [Troubleshooting](Troubleshooting) if the integration itself is unavailable.

## Find The Dongle Address

The easiest method is usually your router's connected-device or DHCP page. Look for a Solplanet/Aiswei device, then create a DHCP reservation so its address does not change.

You can also use the Solplanet app:

1. Open the app and select `+`.
2. Select **Configure Parameters**.
3. Scan the dongle QR code, or load a saved photo of it.
4. Select **Network** while your phone can reach the dongle.
5. Open the dongle details and note its IP address.

## Network Requirements

Home Assistant must be able to reach TCP port 443 or 8484 on the dongle. The devices can be on different VLANs if your firewall allows that traffic. Ping is not required and may be blocked even when the integration works.

The ASW-WLAN-G1 has been used successfully with this integration, but compatibility ultimately depends on the API exposed by its firmware. Our setup process detects the supported protocol rather than relying on the dongle model name.

The dongle may continue connecting to Solplanet cloud services while we use its local API. Blocking its internet access is optional and does not necessarily make local updates faster or more reliable. See [Advanced Local Access](Advanced-Local-Access) before running it offline.

## Change The Update Interval

Open **Settings > Devices & services > Solplanet**, select **Configure**, and enter the new interval in seconds. Start with the 60-second default. Short intervals add load to the dongle and can cause slow or failed updates.
