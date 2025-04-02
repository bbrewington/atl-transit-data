# atl-transit-data

## Overall Flow

1. Cloud Scheduler every 5 minutes --> PubSub
1. EventArc trigger on the PubSub message --> Cloud Run Function with Python code in [marta_realtime/get_data.py](marta_realtime/get_data.py):
    1. Gets data from MARTA Realtime API endpoints trips & vehicles
    1. Parses data with Google's transit module `gtfs_realtime_pb2` --> JSON
    1. Saves parsed JSON to Google Cloud Storage
    1. BigQuery: GCS External Tables --> dbt-managed views to get data in a ready-to-query format

## Accessing Data

This script has been pinging the MARTA Realtime transit data every 5 minutes since April 24, 2024. If you'd like access to either the JSON data in GCS or the data in BigQuery, please contact me at [brent.brewington@gmail.com](mailto:brent.brewington@gmail.com)

## How to run locally

This will ping the MARTA GTFS real-time feed and save one .json from each to GCP project --> GCS bucket

Using uv for Python environment management: ([install link](https://docs.astral.sh/uv/getting-started/installation/))

```bash
git clone https://github.com/bbrewington/atl-transit-data && cd atl-transit-data
uv sync
uv run python get_data.py \
  --project-id YOUR_GCP_PROJECT_ID \
  --bucket-name YOUR_BUCKET_NAME \
  --feeds trip,vehicle
```

## Deployment

The code changes infrequently enough, I don't have CI/CD running for this.  If there are changes to the code here in GitHub, I'll manually deploy it to the Cloud Run functions in my GCP project
