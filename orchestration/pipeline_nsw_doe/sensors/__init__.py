from datetime import timedelta

from dagster import build_last_update_freshness_checks, build_sensor_for_freshness_checks

from pipeline_nsw_doe.assets.raw.assets import raw__nsw_doe_datansw__master_dataset 


checks_freshness_def = build_last_update_freshness_checks(
    assets=[raw__nsw_doe_datansw__master_dataset], lower_bound_delta=timedelta(hours=3),
    deadline_cron="0 1 * * *"
)

sensor_freshness = build_sensor_for_freshness_checks(freshness_checks=checks_freshness_def, minimum_interval_seconds=3600)