"""
MARTA Real-time Data Fetcher

This script fetches real-time GTFS (General Transit Feed Specification) data from MARTA 
(Metropolitan Atlanta Rapid Transit Authority) and uploads it to Google Cloud Storage.
It can fetch trip updates and vehicle positions data.

Usage:
    python get_data.py \
        --project-id=<gcp_project_id> \
        --bucket-name=<gcs_bucket_name> \
        [--feeds=trip,vehicle]
"""

# Python standard library
import json
from datetime import datetime
from argparse import ArgumentParser, Action

# PyPI libraries
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from google.cloud import storage

FEED_NAME_TO_URL = {
    "trip": "https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/tripupdate/tripupdates.pb",
    "vehicle": "https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
}

class SplitArgs(Action):
    """Custom argparse action that splits comma-separated arguments into a list.
    
    Args:
        parser: The ArgumentParser object
        namespace: The namespace to store the argument
        values (str): The comma-separated string value from command line
        option_string: The option string used to invoke this action
        
    Returns:
        None: The result is stored in the namespace
    """
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def get_feed(url):
    """Fetch and parse GTFS real-time data from the specified URL,
    and parses the protobuf response into a dictionary
    
    Args:
        url (str): The URL of the GTFS real-time feed
        
    Raises:
        requests.exceptions.RequestException: If there's an error making the HTTP request
        google.protobuf.message.DecodeError: If there's an error parsing the protobuf message
        
    Returns:
        dict: The parsed GTFS real-time feed as a Python dictionary
        
    Side Effects:
        Makes an HTTP request to an external API
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    feed_result = MessageToDict(feed)
    return feed_result

def save_to_gcs(storage_client, feed_type, url, bucket_name):
    """Fetch GTFS data, format as JSON, and save it to Google Cloud Storage with a timestamped filename
    
    Args:
        storage_client (google.cloud.storage.Client): An initialized GCS client
        feed_type (str): The type of feed ('trip' or 'vehicle')
        url (str): The URL of the GTFS real-time feed
        bucket_name (str): The name of the GCS bucket to upload to
        
    Raises:
        google.cloud.exceptions.GoogleCloudError: If there's an error uploading to GCS
        requests.exceptions.RequestException: If there's an error fetching the feed
        
    Returns:
        None
        
    Side Effects:
        - Makes an HTTP request to an external API
        - Creates a file in Google Cloud Storage
        - Prints a confirmation message to stdout
    """
    bucket = storage_client.bucket(bucket_name)
    current_ts = datetime.now().__format__('%Y%m%d%H%M%S')
    feed_result = get_feed(url)
    
    file_path = f"{feed_type}/{feed_type}_{current_ts}.json"
    blob = bucket.blob(file_path)

    blob.upload_from_string(data=json.dumps(feed_result))

    print(f"File {file_path} uploaded to {bucket_name}")

def get_data(project_id, bucket_name, feeds):
    """Main function to fetch and store MARTA GTFS real-time data.
    Initializes a Google Cloud Storage client and orchestrates
    the fetching and storing of specified GTFS real-time feeds.
    
    Args:
        project_id (str): The Google Cloud project ID
        bucket_name (str): The name of the GCS bucket to upload to
        feeds (list): List of feed types to fetch ('trip', 'vehicle', or both)
        
    Raises:
        google.auth.exceptions.DefaultCredentialsError: If GCP credentials are not available
        google.cloud.exceptions.GoogleCloudError: If there's an error with GCS operations
        requests.exceptions.RequestException: If there's an error fetching the feeds
        
    Returns:
        None
        
    Side Effects:
        - Initializes a GCS client
        - Makes HTTP requests to external APIs
        - Creates files in Google Cloud Storage
        - Prints confirmation messages to stdout
    """
    storage_client = storage.Client(project_id)
    
    feed_dict = {k: v for k, v in FEED_NAME_TO_URL.items() if k in feeds}
    
    for feed_type in feed_dict:
        url = feed_dict[feed_type]
        save_to_gcs(storage_client=storage_client, feed_type=feed_type, url=url, bucket_name=bucket_name)

if __name__ == '__main__':
    feeds = ["trip", "vehicle"]
    
    parser = ArgumentParser()
    parser.add_argument("--project-id")
    parser.add_argument("--bucket-name")
    parser.add_argument("--feeds", default=feeds, action=SplitArgs)
    
    args = parser.parse_args()
    
    assert set(args.feeds).issubset(set(feeds)), f"--feeds must be one of: {', '.join(feeds)}"
    
    get_data(project_id=args.project_id, bucket_name=args.bucket_name, feeds=args.feeds)
