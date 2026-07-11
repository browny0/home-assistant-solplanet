# Quick Start: Charge Or Export On A Schedule

This page is for the two most common jobs:

- Charge your battery from the grid at `X` watts between times `Y` and `Z`.
- Export up to `X` watts between times `Y` and `Z`.

You can do this through the Home Assistant interface. You do not need YAML.

## The Short Version

| Goal | Battery power | Schedule | Extra control |
| --- | --- | --- | --- |
| Charge from grid | Set **Schedule Input Power** to `X` | Add a `charge` slot from `Y` to `Z` | None |
| Export to grid | Set **Schedule Output Power** above `X` to cover house load | Add a `discharge` slot from `Y` to `Z` | Cap the main meter export at `X` |

## Before You Start

Complete [Installation and Setup](Installation-and-Setup), then find these devices under **Settings > Devices & services > Solplanet**:

- Your battery, including **Work mode**, **Schedule Input Power**, **Schedule Output Power**, and **Schedule Configured**.
- Your main meter, if you want to control export.

Home Assistant uses watts. For example, enter `5000` for 5 kW.

`X` is a power rate, not a total amount of energy. Charging at 5 kW for two hours adds roughly 10 kWh before losses, unless the battery reaches **SOC max** first.

> [!IMPORTANT]
> Charging the battery at 5,000 W does not limit your total grid import to 5,000 W. Your house loads are added to the battery charge power.
>
> Setting a 5,000 W export limit caps export at about 5,000 W. It cannot guarantee that amount if your solar and battery do not have enough spare power.

The integration cannot hold your whole property's grid import at an exact watt value. Its import-current control only limits the inverter's own draw.

## Charge From The Grid At X Watts

Example: charge at 5,000 W from 1:00 am to 3:00 am.

### Set The Charging Power

1. Open your Solplanet battery device.
2. Set **Schedule Input Power** to `5000`.
3. Set **Work mode** to **Custom mode**.

### Add The Time Period

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Set Schedule Slots**.
3. Under **Targets**, select the battery's **Schedule Configured** entity.
4. Select the day.
5. Set **Start hour** to `1`.
6. Set **Start minute** to `0`.
7. Set **Duration** to `2`.
8. Set **Mode** to `charge`.
9. Select **Perform action**.
10. Repeat for each day you want to charge.

The schedule remains on the inverter, so you do not need a separate Home Assistant automation to stop charging at 3:00 am.

## Export Up To X Watts

Example: export up to 5,000 W from 5:00 pm to 7:00 pm.

This needs two parts:

1. A battery schedule that makes power available.
2. A meter limit that caps how much reaches the grid.

### Set The Discharging Power

Your house uses battery power before the remainder is exported. Set **Schedule Output Power** high enough to cover both your house load and the export you want.

For example, if you want to export 5,000 W and your house normally uses 1,000 W at that time, start with 6,000 W. Stay within the ratings approved for your system.

1. Open your Solplanet battery device.
2. Set **Schedule Output Power** to `6000` for this example.
3. Set **Work mode** to **Custom mode**.

### Add The Discharge Period

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Set Schedule Slots**.
3. Under **Targets**, select the battery's **Schedule Configured** entity.
4. Select the day.
5. Set **Start hour** to `17`.
6. Set **Start minute** to `0`.
7. Set **Duration** to `2`.
8. Set **Mode** to `discharge`.
9. Select **Perform action**.
10. Repeat for each day you want to export.

### Cap The Export

Test this action manually before adding it to an automation:

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Enable power limit control (Limit power)**.
3. Select your **main meter** as the **Meter device**.
4. Select **Phase-balanced (Sum of all phases)** for a typical single-phase system.
5. Select **(W) absolute power**.
6. Set **Export power limit setpoint (W)** to `5000`.
7. Set **Setpoint offset (W)** to `-100` for a small safety margin.
8. Set **Communications loss timeout** to `60` seconds.
9. Set **Communications loss power limit (W)** to `0` for a conservative fallback.
10. Select **Perform action** and watch your meter power.

Ask your installer which phase mode and fallback values to use if you have a three-phase system or an approved export-control requirement.

### Turn The Export Limit Off At Z

The battery stops scheduled discharge at `Z`, but the export cap stays enabled until you disable it. If you leave it enabled, it can also cap normal daytime solar export.

Test the stop action:

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Disable power limit control**.
3. Select the same main meter.
4. Select **Perform action**.

Create two Home Assistant automations after both manual actions work:

| Automation | Time | Action |
| --- | --- | --- |
| Start export limit | One minute before `Y` | Enable power limit control (Limit power) with the tested values |
| Stop export limit | At `Z` | Disable power limit control |

Open **Settings > Automations & scenes**, create an automation, add a **Time** trigger, then add the tested Solplanet action. Starting the limit one minute early avoids a brief uncapped export when the battery schedule begins.

## Use Your Own Times

The schedule action asks for a start time and duration, not an end time.

| Start (`Y`) | End (`Z`) | Start hour | Start minute | Duration |
| --- | --- | --- | --- | --- |
| 01:00 | 03:00 | `1` | `0` | `2` |
| 13:30 | 16:30 | `13` | `30` | `3` |
| 17:00 | 21:00 | `17` | `0` | `4` |

A slot can start on the hour or half-hour and last one to four whole hours. For a longer period, add adjacent slots. Split a period that crosses midnight between the two days.

The current action labels Tuesday as `Tus` and Wednesday as `Wen`.

## Change Or Remove A Schedule

**Set Schedule Slots** adds a slot. It does not edit an existing one.

To change a slot:

1. Run **Solplanet: Clear Schedule** for that day.
2. Add the day's required slots again.

Wait for a successful integration update and check the existing schedule in the Solplanet app before changing it. This helps avoid losing slots if the dongle's schedule data has not loaded.

## If It Does Not Work

- Confirm the battery is in **Custom mode**.
- Confirm **Schedule Input Power** or **Schedule Output Power** is not 0.
- Confirm you created the slot for the correct day.
- For export control, confirm you selected the main meter.
- Check battery communication, warning, and error entities.
- Disable Power Limit Control temporarily if scheduled charging does not start.

See [Battery Modes and Schedules](Battery-Modes-and-Schedules), [Power Limit Control](Power-Limit-Control), or [Troubleshooting](Troubleshooting) for more detail.
