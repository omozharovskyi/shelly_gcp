CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._all_minutes` AS
WITH time_range AS (
  SELECT
    MIN(minute) AS min_time,
    MAX(minute) AS max_time
  FROM
    `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._minute_grouped`
)
SELECT
  minute
FROM
  time_range,
  UNNEST(GENERATE_TIMESTAMP_ARRAY(min_time, max_time, INTERVAL 1 MINUTE)) AS minute;

CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute_with_zeros` AS
SELECT
  all_minutes.minute,
  IFNULL(energy_minutes.energy_Wh, 0) AS energy_Wh
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._all_minutes` all_minutes
LEFT JOIN
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute` energy_minutes
ON
  all_minutes.minute = energy_minutes.minute
ORDER BY
  all_minutes.minute;