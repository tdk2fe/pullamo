# Uses Boto3, an AWS SDK for Python
import boto3
import json
import argparse
import urllib

# Set up argument parsing with some help text
parser = argparse.ArgumentParser(usage="Simple script to pull and flatten dynamodb values")
parser.add_argument("table_name", help="Table name storing configuration data")
parser.add_argument("application", help="Name of application for which to pull data")
parser.add_argument("environment", help="Name of Environment for which to pull data")
parser.add_argument("primary_region", help="Name of Primary region to check for table in")
parser.add_argument("secondary_region", help="Name of Secondary region to use if primary region fails")
parser.add_argument("config_file", help="JSON file to load into dynamo")
args = parser.parse_args()

# Set arguments
# TODO: Probably add error handling
data_table = args.table_name
application = args.application
environment = args.environment
primary_region = args.primary_region 
secondary_region = args.secondary_region
json_file = args.config_file

def endpoint_check(region='us-east-1'):
    """Function to check if region is up, and if not, try a fallback"""
    url = 'https://dynamodb.' + region + '.amazonaws.com'
    try: 
        r = urllib.request.urlopen(url)
        return True
    except urllib.request.HTTPError:
        return False
    except urllib.request.URLError:
        return False 
    return False

if endpoint_check(primary_region):
    dynamodb = boto3.resource('dynamodb', region_name=primary_region)
else:
    dynamodb = boto3.resource('dynamodb', region_name=secondary_region)

table = dynamodb.Table(data_table)

with open(json_file) as json_file:
    data = json.load(json_file)

data['Application'] = application 
data['Environment'] = environment



response = table.put_item(
    Item = data 
)







