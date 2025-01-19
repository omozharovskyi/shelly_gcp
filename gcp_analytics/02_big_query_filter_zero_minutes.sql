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

CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset.final_results` AS
SELECT
  a.minute,
  IFNULL(e.energy_Wh, 0) AS energy_Wh
FROM
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._all_minutes` a
LEFT JOIN
  `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute` e
ON
  a.minute = e.minute
ORDER BY
  a.minute;