select
  a._FILE_NAME as gcs_file_name,
  b.id as vehicle_id,
  timestamp_seconds(a.header.timestamp) as timestamp,
  -- b.vehicle.timestamp as timestamp2,
  a.header.incrementality,
  a.header.gtfsRealtimeVersion,
  b.vehicle.occupancyStatus,
  b.vehicle.vehicle.label,
  -- b.vehicle.vehicle.id as vehicle_id2,
  b.vehicle.position.speed,
  b.vehicle.position.longitude,
  b.vehicle.position.latitude,
  b.vehicle.position.bearing,
  b.vehicle.trip.scheduleRelationship,
  b.vehicle.trip.directionId,
  b.vehicle.trip.routeId,
  b.vehicle.trip.startDate,
  b.vehicle.trip.tripId,
  ST_GEOGPOINT(b.vehicle.position.longitude, b.vehicle.position.latitude) as geom_point
from {{ source('marta_realtime_data', 'vehicle') }} as a
cross join unnest(a.entity) as b
