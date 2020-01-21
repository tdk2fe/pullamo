import boto3
import json
from faker import Faker
import random

fake = Faker()


ofile = open('output.json', 'w')
chunk = {}

for i in range(10):
    chunk[i] = {}
    nlength = random.randrange(8)
    chunk[i]['name'] = fake.name()
    chunk[i]['email'] = fake.email()
    chunk[i]['address'] = fake.street_address()
    
    chunk[i]['Nested'] = {}
    for j in range(nlength):
        chunk[i]['Nested'][fake.word()] = fake.word() 

json.dump(chunk, ofile)
ofile.close



