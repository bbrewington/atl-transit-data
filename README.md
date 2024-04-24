# atl-transit-data

## How to run

(using "python3" b/c running this on Mac.  For Windows, use "python")

This will ping the MARTA GTFS real-time feed and save one .json from each to GCP project --> GCS bucket

```bash
python3 get_data.py --project-id YOUR_GCP_PROJECT_ID --bucket-name YOUR_BUCKET_NAME --feeds trip,vehicle
```
