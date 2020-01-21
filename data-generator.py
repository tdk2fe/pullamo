import boto3
import json
from faker import Faker
import random

fake = Faker()


ofile = open('output.json', 'w')
chunk = {}

for i in range(10):
    chunk = {}
    nlength = random.randrange(8)
    chunk['name'] = fake.name()
    chunk['email'] = fake.email()
    chunk['address'] = fake.street_address()
    
    chunk['Nested'] = {}
    for j in range(nlength):
        chunk['Nested'][fake.word()] = fake.word() 

    json.dump(chunk, ofile)



ofile.close



