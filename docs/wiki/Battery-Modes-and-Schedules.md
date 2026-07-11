# Battery Modes and Schedules

Use the battery's **Work mode** entity to choose how it operates. Only select a mode supported by your inverter and battery documentation.

## Choose A Work Mode

| Mode | When to use it |
| --- | --- |
| Self-consumption mode | Use solar and battery energy to reduce normal grid consumption. |
| Reserve power mode | Keep more battery energy available as a reserve. |
| Custom mode | Follow charge and discharge periods that you define. |
| Off-grid mode | Operate according to the hardware's supported off-grid behaviour. Do not select this just to disconnect from the Solplanet cloud. |
| Time of use mode | Use the time-of-use settings configured by your system or Solplanet app. |

Our integration can select all five modes, but your hardware may not support every mode. It manages Custom mode schedule slots directly; it does not expose the Solplanet app's full Time of Use configuration.

## Create A Custom Schedule

Custom mode is useful when you want to charge during a cheap tariff, discharge during an expensive period, or prepare the battery for a planned export window.

1. Open the battery device in Home Assistant.
2. Set **Schedule Input Power** to the charging power you want in watts.
3. Set **Schedule Output Power** to the discharging power you want in watts.
4. Set **Work mode** to **Custom mode**.
5. Open **Developer Tools > Actions**.
6. Select **Solplanet: Set Schedule Slots**.
7. Target the battery's **Schedule Configured** binary sensor.
8. Choose the day, start time, duration, and whether the slot should charge or discharge.
9. Perform the action once for each slot you need.

Wait for a successful integration update before changing a schedule, and first confirm that the existing schedule is visible in the Solplanet app. If the dongle's schedule data has not loaded, do not run a schedule action because existing slots may not be retained.

Each call adds one slot to the schedule currently loaded by the integration; it does not intentionally replace existing slots. You can add up to six non-overlapping slots per day. A slot can start on the hour or half-hour and last one to four whole hours. Keep every slot within one day and do not use a duration that carries it past midnight.

The current action labels Tuesday as `Tus` and Wednesday as `Wen`. These labels are expected by the dongle schedule format.

The dongle stores one schedule for the system. Targeting a battery identifies the correct integration, but it does not create a separate schedule for each battery attached to the same inverter.

To remove slots, run **Solplanet: Clear Schedule** against the same **Schedule Configured** entity. Select one day or `all`.

## Create The Same Schedule In The Solplanet App

If you prefer the app:

1. Open the Solplanet app and select `+`.
2. Select **Configure Parameters**.
3. Scan the dongle QR code, or load a saved photo.
4. Select **Network** while your phone can reach the dongle.
5. Open **Energy Storage Settings > Battery Settings > Custom Mode**.
6. Set and save each charge or discharge period and its power.
7. Confirm **Custom Mode** is the active work mode.

Saving a schedule does not activate it unless the battery is also in Custom mode.

## Understand Charge, Discharge, And Export

Scheduled battery discharge power is not the same as grid export. Your house usually consumes battery power first, and only the remainder reaches the grid. A changing house load therefore changes export even when the battery discharge setting stays fixed.

If you need to cap export, use [Power Limit Control](Power-Limit-Control) as well as the battery schedule.

## Reserve Battery Capacity

Use **SOC min** to keep part of the battery in reserve. For example, setting it to 45% should stop normal discharge near 45%, subject to the inverter's own safety behaviour. Lower it later when you want to make that capacity available again.

Use **SOC max** to limit the normal charging target. Do not use either value to override battery protection limits.

## If A Schedule Does Not Work

- Confirm **Custom mode** is still selected.
- Confirm the slot was added to the intended day and did not overlap another slot.
- Check **Schedule Input Power** and **Schedule Output Power**.
- Check battery communication, warning, and error entities.
- Temporarily disable Power Limit Control if it appears to block charging.
- Clear the affected day and recreate its slots if the app and Home Assistant disagree.
