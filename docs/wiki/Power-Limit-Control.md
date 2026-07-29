# Power Limit Control

Power Limit Control lets a supported V2 inverter respond to measurements from the main grid meter. You can use it to cap export, limit the inverter's grid current, or request zero export.

An export limit is a ceiling, not a command to export that amount. A battery Custom mode schedule controls when discharge is requested; Power Limit Control controls how much net power may reach the grid.

This is an advanced feature that changes inverter behaviour. Home Assistant control of it is not a replacement for an approved export-limiting system, breaker, or other electrical protection. Confirm your permitted limits and required control method with your distributor or installer before using it.

## Choose A Permanent Or Temporary Limit

- For an **approved site export limit**, preserve the installer-commissioned control method and leave it enabled. Do not rely on a Home Assistant automation to enforce a connection requirement unless the installer or distributor has explicitly approved that design.
- For an **optional permanent limit**, configure it in the Solplanet app or set the persistent inverter value through Home Assistant, then leave it enabled and let the battery schedule control when discharge occurs.
- Use a **temporary limit** when the site is permitted to export more at other times and the lower ceiling is needed only for a tariff window. Home Assistant can enable it at the start and disable it at the end.

Do not automate disabling a distributor- or installer-required export limit. If you do not know whether a setting is required for connection approval, ask the installer or distributor before changing it.

## Choose A Control Mode

| Action | What it does |
| --- | --- |
| Enable power limit control (Limit power) | Caps export using an absolute watt value or a percentage of inverter rating. |
| Enable power limit control (Limit current) | Sets maximum export and import current for the inverter. |
| Enable power limit control (Zero power) | Asks the inverter to avoid exporting to the grid. |
| Disable power limit control | Disables the active power-limit mode. |

Only one mode can be active. Running a different enable action replaces the previous mode.

## Apply A Limit

### In The Solplanet App

1. Open the local **Configure Parameters** flow.
2. Select the E-meter and open **Export active power control**.
3. Enable the control and select the phase mode and absolute-watt or percentage target required for the installation.
4. If exposed, set the communications-loss values required for the installation.
5. Save the settings and verify the result at the physical or retailer meter.

This may require an installer account, the dongle QR code, and a phone on the same network as the dongle. The saved limit is persistent; the app does not need to remain open.

### In Home Assistant

1. Open **Developer Tools > Actions**.
2. Search for **Solplanet** and select the action you need.
3. In **Meter device**, select the main Solplanet meter, not the inverter, battery, dongle, or a sub-meter.
4. Enter conservative limits and complete every required field.
5. Perform the action.
6. If available, open the meter device and check the **Power limit control** diagnostic entity.
7. Watch meter power and battery behaviour to confirm the result on your system.

If you automate a temporary limit, add **Disable power limit control** at the end of the automation so the system does not remain in that mode unexpectedly. Do not add that action for a permanent approved limit.

## Limit Export Power

Use **Limit power** when you want a watt or percentage cap. For a controlled battery export window, you can set a Custom mode discharge period and then use this action to cap the excess power reaching the grid after the house load is served.

For example, if the inverter, battery/BMS, and installation all support 10,000 W, a system with a 5,000 W export ceiling can use **Schedule Output Power** up to 10,000 W. The battery can then cover house load plus the grid target, while Power Limit Control holds net export near the ceiling. Setting Schedule Output Power to only 5,000 W would make the house consume part of that amount and reduce grid export.

Choose whether the target applies to the sum of all phases or to each phase. Use the option required for your installation and export approval. If you are unsure, ask your installer.

An absolute target cannot exceed the inverter rating detected by the integration. Percentage targets can range from 0% to 100%.

## Limit Grid Current

Use **Limit current** to set both maximum export current and maximum import current for the inverter. This can reduce battery charging demand when other appliances are using a large amount of grid power.

The import value only limits the inverter's own grid draw. It cannot stop other household loads from exceeding the service or breaker rating.

## Use A Setpoint Offset

An offset gives the inverter some headroom around the target. For example, a 5,000 W export target with a -200 W offset aims below the hard limit, which can help with brief overshoot when house load changes.

Start with a small conservative offset and verify the actual meter reading. Do not assume the effective result is identical on every firmware version.

## Communications Loss Fields

The actions expose vendor settings for a PLC communications-loss timeout and fallback limit. These settings belong to the inverter and meter control path; they are not a watchdog for Home Assistant or the dongle connection.

Use a conservative fallback value. Do not rely on these fields until you have tested how your inverter and firmware behave when meter communication is interrupted.

## Known Behaviour

- Power Limit Control is available only on supported V2 systems with a main meter.
- Some firmware exposes a simpler percentage-only E-meter control protocol. **Configure power limit control (404 compatibility)** is a separate Home Assistant action; run it only when the standard **Limit power** action returns HTTP 404.
- Some systems and firmware combinations have prevented grid or PV battery charging while a limit was active. Other systems on similar firmware have worked normally, so test the exact installation.
- Some systems have needed the absolute **Export power limit setpoint (W)** set to 0 in **Limit power** mode before the control could be disabled successfully.
- Three-phase and multi-meter behaviour depends on the installation and firmware. We expose controls only for the main meter.
- While enabled, Power Limit Control applies continuously to all export in the Solplanet control path, including battery discharge and excess DC-coupled solar.
- It cannot directly curtail an unrelated AC-coupled solar inverter unless the installation includes compatible site-wide control.
- Firmware or Solplanet-side changes can alter behaviour without a Home Assistant configuration change.

If an optional temporary limit prevents scheduled charging, disable it and check [Troubleshooting](Troubleshooting). If the limit enforces an approved site ceiling, do not remove it as a workaround; contact the installer or Solplanet. Re-test after inverter, battery, or Solplanet-side changes.

## Official Reference

- [Solplanet App User Manual](https://solplanet.net/wp-content/uploads/2025/11/UM0072_Solplanet-App_EN_V02.pdf)
