select
  a._file_name as gcs_file_name,
  b.id as trip_id,
  c.scheduleRelationship,
  c.stopSequence,
  -- ifnull(c.stopTimeProperties, '') as stopTimeProperties,
  c.stopId,
  timestamp_seconds(c.departure.time) as departure_time,
  timestamp_seconds(c.arrival.time) as arrival_time,

FROM `data-projects-348920.marta_realtime_data.trip` as a
cross join unnest(a.entity) as b
cross join unnest(b.tripUpdate.stopTimeUpdate) as c
