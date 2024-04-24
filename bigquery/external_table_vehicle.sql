CREATE EXTERNAL TABLE IF NOT EXISTS
`data-projects-348920.marta_realtime_data.vehicle`
  OPTIONS (
    format ="JSON",
    uris = ['gs://marta-realtime-data/vehicle/*.json']
    );
