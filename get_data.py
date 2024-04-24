# Python standard library
import json
from datetime import datetime
from argparse import ArgumentParser, Action

# Local
from constants import FEED_NAME_TO_URL

# PyPI libraries
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from google.cloud import storage

class SplitArgs(Action):
    """This is used in argparse - splits comma-separated args
    """
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def get_feed(url):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    feed_result = MessageToDict(feed)
    return feed_result

def save_to_gcs(storage_client, feed_type, url, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    current_ts = datetime.now().__format__('%Y%m%d%H%M%S')
    feed_result = get_feed(url)
    
    file_path = f"{feed_type}/{feed_type}_{current_ts}.json"
    blob = bucket.blob(file_path)

    blob.upload_from_string(data=json.dumps(feed_result))

    print(f"File {file_path} uploaded to {bucket_name}")

def get_data(project_id, bucket_name, feeds):
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
