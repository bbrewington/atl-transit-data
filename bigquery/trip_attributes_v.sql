SELECT
  a._FILE_NAME as gcs_file_name,
  timestamp_seconds(a.header.timestamp) as header_timestamp,
  a.header.incrementality,
  a.header.gtfsRealtimeVersion,
  b.id as trip_id,
  timestamp_seconds(b.tripupdate.timestamp) as trip_timestamp,
  b.tripUpdate.tripProperties.startDate as trip_start_date,
  b.tripUpdate.tripProperties.startTime as trip_start_time,
  b.tripUpdate.vehicle.id as vehicle_id,
  b.tripUpdate.vehicle.label as vehicle_label,
  b.tripUpdate.trip.directionId as trip_direction_id,
  b.tripUpdate.trip.routeId as trip_route_id,
  -- b.tripUpdate.trip.startDate as trip_start_date2,
  -- b.tripUpdate.trip.startTime as trip_start_time2,
  b.tripUpdate.trip.scheduleRelationship as trip_schedule_relationship,
  -- b.tripUpdate.trip.tripId as trip_id2,
FROM `data-projects-348920.marta_realtime_data.trip` as a
cross join unnest(a.entity) as b
