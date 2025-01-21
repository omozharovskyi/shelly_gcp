CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._tree_zones_tariff_hourly_kyiv_total` AS
SELECT
  hour_of_day_kyiv,
  total_energy_Wh,
  total_energy_Wh / 1000 as total_energy_kWh,
  total_energy_Wh * 4.32 / 1000 AS cost_1_zone,  -- 1 Zone tariff
  CASE  -- 2 Zones tariff
    WHEN hour_of_day_kyiv BETWEEN 23 AND 24 OR hour_of_day_kyiv BETWEEN 0 AND 7 THEN total_energy_Wh * 2.16 / 1000
    ELSE total_energy_Wh * 4.32 / 1000
  END AS cost_2_zone,
  CASE  -- 3 Zones tariff
    WHEN hour_of_day_kyiv BETWEEN 23 AND 24 OR hour_of_day_kyiv BETWEEN 0 AND 7 THEN total_energy_Wh * 1.73 / 1000
    WHEN hour_of_day_kyiv BETWEEN 8 AND 11 OR hour_of_day_kyiv BETWEEN 20 AND 22 THEN total_energy_Wh * 6.48 / 1000
    ELSE total_energy_Wh * 4.32 / 1000
  END AS cost_3_zone
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._hourly_energy_consumption_kyiv`;


SELECT sum(cost_1_zone), sum (cost_2_zone), sum(cost_3_zone)
FROM `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._tree_zones_tariff_hourly_kyiv_total`;

SELECT hour_of_day_kyiv, cost_1_zone, cost_2_zone, cost_3_zone
FROM `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._tree_zones_tariff_hourly_kyiv_total` order by hour_of_day_kyiv asc;