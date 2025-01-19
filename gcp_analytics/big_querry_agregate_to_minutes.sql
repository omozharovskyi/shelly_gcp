CREATE OR REPLACE  TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._minute_grouped` AS
SELECT
  TIMESTAMP_MILLIS(CAST(`timestamp` AS INT64)) AS timestamp,
  TIMESTAMP_TRUNC(TIMESTAMP_MILLIS(CAST(`timestamp` AS INT64)), MINUTE) AS minute,
  aprt_power
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset.external_shelly_gcp_agregated_mqtt`
ORDER BY
  timestamp;

CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._lead_values` AS
SELECT
  minute,
  aprt_power,
  LEAD(aprt_power) OVER (PARTITION BY minute ORDER BY timestamp) AS next_aprt_power,
  timestamp,
  LEAD(timestamp) OVER (PARTITION BY minute ORDER BY timestamp) AS next_timestamp
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._minute_grouped`;

CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute` AS
SELECT
  minute,
  SUM(0.5 * (next_aprt_power + aprt_power) * TIMESTAMP_DIFF(next_timestamp, timestamp, SECOND) / 3600) / 1000 AS energy_kWh
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._lead_values`
WHERE
  next_timestamp IS NOT NULL
GROUP BY
  minute;
