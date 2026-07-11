# Power Limit Control

Power Limit Control lets a supported V2 inverter respond to measurements from the main grid meter. You can use it to cap export, limit the inverter's grid current, or request zero export.

This is an advanced feature that changes inverter behaviour. It is not a replacement for an approved export-limiting system, breaker, or other electrical protection. Confirm your permitted limits with your distributor or installer before using it.

## Choose A Control Mode

| Action | What it does |
| --- | --- |
| Enable power limit control (Limit power) | Caps export using an absolute watt value or a percentage of inverter rating. |
| Enable power limit control (Limit current) | Sets maximum export and import current for the inverter. |
| Enable power limit control (Zero power) | Asks the inverter to avoid exporting to the grid. |
| Disable power limit control | Disables the active power-limit mode. |

Only one mode can be active. Running a different enable action replaces the previous mode.

## Apply A Limit

1. Open **Developer Tools > Actions**.
2. Search for **Solplanet** and select the action you need.
3. In **Meter device**, select the main Solplanet meter, not the inverter, battery, dongle, or a sub-meter.
4. Enter conservative limits and complete every required field.
5. Perform the action.
6. If available, open the meter device and check the **Power limit control** diagnostic entity.
7. Watch meter power and battery behaviour to confirm the result on your system.

If you automate a temporary limit, add **Disable power limit control** at the end of the automation so the system does not remain in that mode unexpectedly.

## Limit Export Power

Use **Limit power** when you want a watt or percentage cap. For a controlled battery export window, you can set a Custom mode discharge period and then use this action to cap the excess power reaching the grid after the house load is served.

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
- Some firmware versions have prevented grid or PV battery charging while a limit was active.
- Some systems have needed the absolute **Export power limit setpoint (W)** set to 0 in **Limit power** mode before the control could be disabled successfully.
- Three-phase and multi-meter behaviour depends on the installation and firmware. We expose controls only for the main meter.
- Firmware or Solplanet-side changes can alter behaviour without a Home Assistant configuration change.

Disable the limit before a scheduled charge if charging does not start, then check [Troubleshooting](Troubleshooting). Re-test your automations after inverter or battery firmware changes.
