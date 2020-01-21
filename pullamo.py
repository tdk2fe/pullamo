# Uses Boto3, an AWS SDK for Python
import boto3
import json
import argparse

# Set up argument parsing with some help text
parser = argparse.ArgumentParser(usage="Simple script to pull and flatten dynamodb values")
parser.add_argument("TableName", help="Table name storing configuration data")
parser.add_argument("Application", help="Name of application for which to pull data")
parser.add_argument("Environment", help="Name of Environment for which to pull data")
parser.add_argument("PrimaryRegion", help="Name of Primary region to check for table in")
parser.add_argument("SecondaryRegion", help="Name of Secondary region to use if primary region fails")
args = parser.parse_args()

# Set arguments
# TODO: Probably add error handling
data_table = args.TableName
application = args.Application
environment = args.Environment
primary_region = args.PrimaryRegion 
secondary_region = args.SecondaryRegion

try:
    # Create a DDB resource and table object
    dynamodb = boto3.resource('dynamodb', region_name=primary_region)
    table = dynamodb.Table(data_table)

    # Get an item - need to have both App and Env
    # Since it is a composite key
    response = table.get_item(
        Key={
            'Application': application,
            'Environment': environment
        }
    )
except:
    # Create a DDB resource and table object
    dynamodb = boto3.resource('dynamodb', region_name=secondary_region)
    table = dynamodb.Table(data_table)

    # Get an item - need to have both App and Env
    # Since it is a composite key
    response = table.get_item(
        Key={
            'Application': application,
            'Environment': environment
        }
    )


# Recursive function to flatten nexted items in the table
# Parent -> Nest1 -> Nest2 would become Parent_Nest1_Nest2
def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out
    
item = response['Item']
flat = flatten_json(item)

# Print the output suitable for exporting in a *Nix environment
for k in flat:
    stripflat = str(flat[k]).strip()
    print('export ' + k.upper() + '="' + stripflat + '"')

