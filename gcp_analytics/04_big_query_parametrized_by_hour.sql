DECLARE date_range STRING DEFAULT 'all_time';  -- 'all_time', 'last_30_days', 'current_month', 'specific_month'

CREATE OR REPLACE TABLE `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._hourly_energy_consumption_kyiv` AS
WITH filtered_data AS (
  SELECT
    minute,
    energy_Wh
  FROM
    `shelly-gcp-data-analytics.bq_shelly_gcp_dataset._energy_per_minute_with_zeros`
  WHERE
    (date_range = 'all_time' AND TRUE) OR
    (date_range = 'last_30_days' AND minute >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)) OR
    (date_range = 'current_month' AND EXTRACT(YEAR FROM minute) = EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM minute) = EXTRACT(MONTH FROM CURRENT_DATE())) OR
    (date_range = 'specific_month' AND EXTRACT(YEAR FROM minute) = 2021 AND EXTRACT(MONTH FROM minute) = 5)  -- May 2021
)
SELECT
  EXTRACT(HOUR FROM minute AT TIME ZONE "Europe/Kiev") AS hour_of_day_kyiv,
  SUM(energy_Wh) AS total_energy_Wh
FROM
  filtered_data
GROUP BY
  hour_of_day_kyiv
ORDER BY
  hour_of_day_kyiv;