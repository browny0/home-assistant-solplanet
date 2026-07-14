# Quick Start: Charge Or Export On A Schedule

This page is for the two most common jobs:

- Charge your battery from the grid at `X` watts between times `Y` and `Z`.
- Export up to `X` watts between times `Y` and `Z`.

For a fixed repeating schedule, the Solplanet app is usually the simplest option. The schedule runs on the Solplanet system and does not need Home Assistant to start or stop it. Use Home Assistant when you need a temporary meter limit, conditions such as battery SOC, or other dynamic behaviour. You do not need YAML for either path.

## The Short Version

| Goal | Battery power | Schedule | Extra control |
| --- | --- | --- | --- |
| Charge from grid | Set **Schedule Input Power** to `X` | Add a `charge` slot from `Y` to `Z` | None |
| Export to grid | Set **Schedule Output Power** above `X` to cover house load | Add a `discharge` slot from `Y` to `Z` | Cap the main meter export at `X` |

## Choose App Only Or Home Assistant

- **Solplanet app only:** Use Custom mode for fixed charge and discharge periods. Add a permanent E-meter export limit if you always want the same export ceiling.
- **Home Assistant:** Use it only when the export limit must be enabled for part of the day, or when you want conditions such as SOC, load, price, or tariff state.

Power Limit Control is a ceiling, not a request to export. By design, a permanent 5,000 W limit does not force the system to export 5,000 W outside a scheduled discharge period.

## Before You Start

For the Home Assistant path, complete [Installation and Setup](Installation-and-Setup), then find these devices under **Settings > Devices & services > Solplanet**:

- Your battery, including **Work mode**, **Schedule Input Power**, **Schedule Output Power**, and **Schedule Configured**.
- Your main meter, if you want to control export.

If you are configuring the schedule entirely in the Solplanet app, you do not need to install the integration. Follow [Create The Same Schedule In The Solplanet App](Battery-Modes-and-Schedules#create-the-same-schedule-in-the-solplanet-app). Access to E-meter settings may require installer or local **Configure Parameters** permissions.

Home Assistant uses watts. For example, enter `5000` for 5 kW.

`X` is a power rate, not a total amount of energy. Charging at 5 kW for two hours adds roughly 10 kWh before losses, unless the battery reaches **SOC max** first.

> [!IMPORTANT]
> Charging the battery at 5,000 W does not limit your total grid import to 5,000 W. Your house loads are added to the battery charge power.
>
> Setting a 5,000 W export limit caps export at about 5,000 W. It cannot guarantee that amount if your solar and battery do not have enough spare power.

The integration cannot hold your whole property's grid import at an exact watt value. Its import-current control only limits the inverter's own draw.

## Charge From The Grid At X Watts

Example: charge at 5,000 W from 1:00 am to 3:00 am.

In the Solplanet app, set the charging power and add the charge period under **Battery Settings > Custom Mode**. Leave Custom mode active. The equivalent Home Assistant steps are below.

### Set The Charging Power In Home Assistant

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

The schedule remains on the Solplanet system, so you do not need a Home Assistant automation to start or stop charging. For the ASW008K/010K-SH, Solplanet documents that Custom mode operates as Self-consumption mode outside configured charge and discharge periods. Check the inverter manual for other models.

## Export Up To X Watts

Example: export up to 5,000 W from 5:00 pm to 7:00 pm.

This needs two parts:

1. A battery schedule that makes power available.
2. A meter limit that caps how much reaches the grid.

### Set The Discharging Power

Your house uses battery power before the remainder is exported. Set **Schedule Output Power** high enough to cover both your house load and the export you want.

For example, if you want to export 5,000 W and your house normally uses 1,000 W at that time, start with 6,000 W. Stay within the ratings approved for your system.

If Power Limit Control is capping grid export, you can instead set **Schedule Output Power** up to the lowest supported limit of the inverter, battery/BMS, and installation. For example, if all parts of a 10,000 W system support that rate, a 5,000 W meter limit can leave up to 10,000 W available so the battery can cover changing house load as well as the export target. The meter limit then caps what reaches the grid.

1. Open your Solplanet battery device.
2. Set **Schedule Output Power** to `6000` for the house-load estimate above, or use the lowest supported inverter, battery/BMS, and installation limit when a tested meter limit will cap grid export.
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

For an app-only setup, open the Solplanet app's local **Configure Parameters** flow, select the E-meter, enable export active power control, choose the required phase and absolute-watt settings, enter the permitted export limit, and save it. This setting remains active until it is changed or disabled.

Account permissions and menu labels vary. You may need an installer account, a saved photo of the dongle QR code, and a phone connected to the same network as the dongle.

To test the same control through Home Assistant before automating it:

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Enable power limit control (Limit power)**.
3. Select your **main meter** as the **Meter device**.
4. Select **Phase-balanced (Sum of all phases)** for a typical single-phase system.
5. Select **(W) absolute power**.
6. Set **Export power limit setpoint (W)** to `5000`.
7. For an optional test, `-100` is an example **Setpoint offset (W)**. Preserve a commissioned value or use the value required by your installer.
8. For an optional test, `60` seconds is an example **Communications loss timeout**. Preserve a commissioned value or use the required value.
9. For an optional test, `0` is a conservative example **Communications loss power limit (W)**. Do not replace an approved fallback value without installer guidance.
10. Select **Perform action** and watch your meter power.

Ask your installer which phase mode and fallback values to use if you have a three-phase system or an approved export-control requirement.

### Decide Whether The Export Limit Is Permanent

The battery stops scheduled discharge at `Z`, but the export ceiling remains enabled until you disable it. That is normally desirable when it is your approved site export limit or your intended permanent ceiling. On models documented to use Self-consumption outside Custom mode slots, the limit does not itself request further battery export.

> [!IMPORTANT]
> Do not automate the removal of a distributor- or installer-required export limit. Confirm whether a limit is an installation requirement before disabling it.

While enabled, the ceiling applies continuously to all export that the Solplanet system can control, including battery discharge and excess DC-coupled solar. It cannot directly curtail an unrelated AC-coupled solar inverter unless the installation includes compatible site-wide control.

If your site is permitted to export more outside the scheduled period and you intentionally want a temporary tariff limit, test the stop action:

1. Open **Developer Tools > Actions**.
2. Select **Solplanet: Disable power limit control**.
3. Select the same main meter.
4. Select **Perform action**.

Create two Home Assistant automations only after both manual actions work:

| Automation | Time | Action |
| --- | --- | --- |
| Start export limit | At `Y` | Enable power limit control (Limit power) with the tested values |
| Stop export limit | At `Z` | Disable power limit control |

Open **Settings > Automations & scenes**, create an automation, add a **Time** trigger, then add the tested Solplanet action. The Solplanet Custom mode schedule already controls charging, discharging, and the return to Self-consumption behaviour. Do not add boundary actions that reset **Schedule Input Power**, **Schedule Output Power**, or **Work mode** unless you deliberately want Home Assistant to override the device schedule.

If the export ceiling is permanent, do not create these automations. Leave the limit enabled and let the Solplanet schedule control when the battery discharges.

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
- Test scheduled charging while Power Limit Control is enabled. Behaviour differs between otherwise similar inverter and firmware combinations.
- If an optional temporary limit blocks charging, disable it and re-test. If it enforces an approved site limit, do not remove it without installer or distributor guidance.

See [Battery Modes and Schedules](Battery-Modes-and-Schedules), [Power Limit Control](Power-Limit-Control), or [Troubleshooting](Troubleshooting) for more detail.
