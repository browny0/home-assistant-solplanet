# Energy Dashboard

Home Assistant's Energy dashboard shows how much energy your solar system produces, how much you import or export, and how much enters or leaves your battery.

The Energy dashboard uses energy values measured in kilowatt-hours (kWh). Do not select live power entities measured in watts (W) for the energy fields.

## Recommended Entities

Choose the entities that match your system. Their entity IDs may differ, so select them by their displayed names.

| Energy dashboard field | V2 entity | V1 entity |
| --- | --- | --- |
| Grid consumption | **Total grid supplied** | **Grid energy in total** |
| Return to grid | **Total grid feed-in** | **Grid energy out total** |
| Battery energy incoming | **Battery energy for charging** | **Battery energy for charging** |
| Battery energy outgoing | **Battery energy for discharging** | **Battery energy for discharging** |

For solar production, use **PV energy total** from the battery device on a typical hybrid system. If that entity is unavailable and the inverter reports solar-only production, use **Energy produced total** from the inverter.

Do not add two entities that measure the same solar panels. This would count the production twice.

## Add The Grid

1. Open **Settings > Dashboards > Energy**.
2. Find **Grid consumption** and add a source.
3. Set **Energy imported from the grid** to **Total grid supplied**, or **Grid energy in total** on V1.
4. Set **Energy exported to the grid** to **Total grid feed-in**, or **Grid energy out total** on V1.
5. Add your import and export prices if you want Home Assistant to estimate costs and returns.
6. Save the configuration.

Use the main meter entities. Do not use a discovered sub-meter unless it genuinely measures a separate grid connection and provides its own energy values.

## Add Solar Production

1. Find **Solar panels** in the Energy configuration.
2. Add **PV energy total** for a hybrid inverter and battery system.
3. If **PV energy total** is unavailable, add **PV energy today** or the inverter's **Energy produced total**, whichever represents solar production on your installation.
4. Save the configuration.

For a hybrid inverter, total inverter output can include energy discharged from the battery. Using that value as solar production can count stored energy as new solar energy. Compare your chosen entity with the Solplanet app over a full day before relying on it.

If you have a separate solar inverter that is not monitored by this integration, use the production entity from that inverter instead.

## Add The Battery

1. Find **Home battery storage** in the Energy configuration.
2. Set **Energy going into the battery** to **Battery energy for charging**.
3. Set **Energy coming out of the battery** to **Battery energy for discharging**.
4. Save the configuration.

If you have multiple battery devices, check whether each entity reports an independent stack or repeats the total for the whole system. Add independent stack counters, but add only one entity if every battery repeats the same system total.

## Wait For Statistics

The Energy dashboard is not a live-power dashboard. Home Assistant builds it from long-term statistics, so new data may take up to an hour to appear. Data recorded before you configure the dashboard may appear, but Home Assistant cannot recover periods from before the integration was installed.

Use the normal Solplanet device entities when you want to watch live power.

## If An Entity Is Missing

1. Open **Settings > Developer tools > States**.
2. Find the energy entity and confirm it has a value in `kWh`.
3. Open **Settings > Developer tools > Statistics** and resolve any issue shown for that entity.
4. Confirm Recorder has not been configured to exclude the entity.
5. Allow at least two integration updates, then check the Energy configuration again.

Use a total energy entity when one is available. Daily entities such as **E-grid supplied**, **E-grid feed-in**, and **PV energy today** reset each day and are best kept as fallbacks.

## If The Totals Look Wrong

- Compare full-day totals rather than live power at a single moment.
- Confirm you did not add the same solar array or battery counter twice.
- Compare grid import and export with your electricity meter or retailer data.
- Check the CT clamp and meter installation if import and export appear reversed.
- Remember that loads outside the Solplanet meter's measurement point will not be included.

Home Assistant calculates the energy-flow diagram from the sources you add. Our integration does not provide a separate house-load energy entity.

See the [Home Assistant energy documentation](https://www.home-assistant.io/docs/energy/) for tariffs, pricing, solar forecasts, and other Energy dashboard features.
