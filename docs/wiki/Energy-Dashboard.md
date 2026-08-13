# Energy Dashboard

Home Assistant's Energy dashboard shows how much energy your solar system produces, how much you import or export, and how much enters or leaves your battery (if you have one).

The Energy dashboard has two main views that need different sensors:

- **Electricity** (`/energy/electricity`) — the historical charts. It needs energy values measured in kilowatt-hours (kWh). This view works without live-power entities.
- **Now** (`/energy/now`) — the live flow diagram. It needs the same energy sources **plus** a live power entity (W) for each source. If no power entity is configured, the view is empty even when the historical charts work.

Do not select live power entities (W) for the energy (kWh) fields. Power entities belong in the separate **Power measurement** field on each source.

Single-phase and three-phase systems use the same total-power entities. Per-phase entities (for example, **AC phase 1 power**) are diagnostic only and should not be used in the Energy dashboard.

## Recommended Entities

Choose the entities that match your system. Their entity IDs may differ, so select them by their displayed names. Skip any section that does not apply to your installation.

### Energy fields (kWh)

| Energy dashboard field | V2 entity | V1 entity |
| --- | --- | --- |
| Grid consumption | **Total grid supplied** | **Grid energy in total** |
| Return to grid | **Total grid feed-in** | **Grid energy out total** |
| Battery energy incoming (if you have a battery) | **Battery energy for charging** | **Battery energy for charging** |
| Battery energy outgoing (if you have a battery) | **Battery energy for discharging** | **Battery energy for discharging** |

For solar production, use **PV energy total** from the battery device on a typical hybrid system. If you do not have a battery device, or **PV energy total** is unavailable and the inverter reports solar-only production, use **Energy produced total** from the inverter.

Do not add two entities that measure the same solar panels. This would count the production twice.

### Power measurement fields (W) — required for `/energy/now`

| Power measurement field | V2 entity | V1 entity |
| --- | --- | --- |
| Grid power | **Meter power** (this integration) or your meter's power entity | **Grid power** (this integration) or your meter's power entity |
| Solar power (hybrid with battery) | **PV power** (battery device) | **PV power** (battery device) |
| Solar power (solar-only, no battery) | **Power** (inverter device) | **Power** (inverter device) |
| Battery power (if you have a battery) | **Battery power** | **Battery power** |

If your meter comes from a different Home Assistant integration, select its power entity in the **Power measurement** field instead. The friendly name will differ (for example, an EASTRON meter appears as **EASTRON SDM230-Modbus V1 Meter power**).

Power entities follow the Home Assistant Energy dashboard convention: grid positive = importing, battery positive = discharging, solar positive = producing. The **Type of power measurement** dropdown offers **Standard** (entity already follows this convention) and **Inverted** (HA will flip the sign). Use **Standard** if your entity already matches the convention above; switch to **Inverted** if it does not.

If you are unsure which value to pick, force a clear charging or discharging moment and watch **Developer tools > States** while it is happening. The Solplanet `battery_power` sensor does not document its sign convention, so it is worth checking both interpretations against the battery state of charge and the Solplanet app before relying on the value.

## Add The Grid

1. Open **Settings > Dashboards > Energy**.
2. Find **Grid consumption** and add a source.
3. Set **Energy imported from the grid** to **Total grid supplied**, or **Grid energy in total** on V1.
4. Set **Energy exported to the grid** to **Total grid feed-in**, or **Grid energy out total** on V1.
5. Set **Power measurement** to the power entity for your grid meter (**Meter power** on V2, **Grid power** on V1, or the equivalent from your meter integration). This is required for the live `/energy/now` view.
6. Add your import and export prices if you want Home Assistant to estimate costs and returns.
7. Save the configuration.

Use the main meter entities. Do not use a discovered sub-meter unless it genuinely measures a separate grid connection and provides its own energy values.

## Add Solar Production

1. Find **Solar panels** in the Energy configuration.
2. Add **PV energy total** from the battery device on a hybrid system.
3. If you do not have a battery device, or **PV energy total** is unavailable, add **PV energy today** or the inverter's **Energy produced total**, whichever represents solar production on your installation.
4. Set **Power measurement** to **PV power** from the battery device on a hybrid system. On a solar-only inverter without a battery device, use **Power** from the inverter device. This is required for the live `/energy/now` view.
5. Save the configuration.

For a hybrid inverter, total inverter output can include energy discharged from the battery. Using that value as solar production can count stored energy as new solar energy. Compare your chosen entity with the Solplanet app over a full day before relying on it.

If you have a separate solar inverter that is not monitored by this integration, use the production entity from that inverter instead.

## Add The Battery

Skip this section if your installation does not include a battery.

1. Find **Home battery storage** in the Energy configuration.
2. Set **Energy going into the battery** to **Battery energy for charging**.
3. Set **Energy coming out of the battery** to **Battery energy for discharging**.
4. Set **Power measurement** to **Battery power**. This is required for the live `/energy/now` view.
5. Optionally add the battery state-of-charge sensor to enable the SOC badge in the live view.
6. Save the configuration.

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
