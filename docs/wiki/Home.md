# Solplanet Home Assistant Integration

Our integration connects Home Assistant directly to a Solplanet or Aiswei inverter dongle on your local network. You can monitor your solar and battery system without relying on the Solplanet cloud, then use Home Assistant to manage supported battery and grid controls.

## What You Can Do

- View inverter production, battery state of charge, and grid import or export.
- Change the battery work mode and state-of-charge limits.
- Set charge and discharge power for Custom mode schedules.
- Create and clear battery schedule slots.
- Limit grid export, limit inverter grid current, or enable zero-export mode on supported V2 systems.
- Use the entities and actions in dashboards, scripts, and automations.

The exact entities available depend on your inverter, battery, meter, dongle, and firmware. Our main development focus is V2 hardware and firmware. V1 devices have fewer features.

## Getting Started

- [Installation and Setup](Installation-and-Setup): connect Home Assistant to your dongle.
- [Quick Start](Quick-Start): charge or export a chosen amount during a set time period.
- [Energy Dashboard](Energy-Dashboard): add your solar, grid, and battery history to Home Assistant.

## Guides

- [Battery Modes and Schedules](Battery-Modes-and-Schedules): choose a work mode and manage charge or discharge periods.
- [Power Limit Control](Power-Limit-Control): control supported grid import and export behaviour.

## Reference

- [Entities and Actions](Entities-and-Actions): understand the devices, entities, and actions we provide.

## Help And Advanced Use

- [Troubleshooting](Troubleshooting): resolve connection, data, meter, battery, and action problems.
- [Advanced Local Access](Advanced-Local-Access): test local endpoints, run without cloud access, and understand dongle security.

For normal use, you only need the dongle's IP address or hostname. You do not need a Solplanet cloud account, installer password, QR code, or inverter serial number.

## Before You Change Settings

Some controls can stop the inverter or battery, change when the battery charges, or alter grid import and export. Before using them, confirm your distributor export limit and any installation-specific restrictions with your installer or electrician.

Start with conservative values and watch the system after every change. Do not use Home Assistant as a substitute for required electrical protection or an approved export-limiting device.

Do not share photos of the dongle QR code or password label. Treat the dongle as a trusted local-network device and restrict access to it.
