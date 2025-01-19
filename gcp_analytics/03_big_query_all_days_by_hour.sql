CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._hourly_energy_consumption_utc` AS
SELECT
  EXTRACT(HOUR FROM minute) AS hour_of_day,
  SUM(energy_Wh) AS total_energy_Wh
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute_with_zeros`
GROUP BY
  hour_of_day
ORDER BY
  hour_of_day;


CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._hourly_energy_consumption_kyiv` AS
SELECT
  EXTRACT(HOUR FROM TIMESTAMP(minute, "Europe/Kiev")) AS hour_of_day_kyiv,
  SUM(energy_kWh) AS total_energy_kWh
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute_with_zeros`
GROUP BY
  hour_of_day_kyiv
ORDER BY
  hour_of_day_kyiv;