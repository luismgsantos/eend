# I have a csv file with 140k+ rows of data.
# i want to create another csv file with some of the data from the file and making an http request to a website foreach row
# and get the response and add it to the new csv file.
# I want to do this in the most efficient way possible.
# the csv header is: postal_code,street,house_numbers,city,area,neighborhood,municipality,province
# the api that i have to consume gives me the 'providers' for each row.
# the resulting csv has to have the following header
#postal_code,street,city,neighborhood,municipality,province,provider
# the api endpoint is: https://geo.api.mijnaansluiting.nl/api

import csv
from time import sleep

import requests
import json
import sys

reader = csv.DictReader(open('/Users/lsantos/Sites/personal/eend/split/output_%s.csv' % sys.argv[1], 'r'))
# output the first 2 line fo the file
# open the file in the write mode
outputFile = open('./done/%s.csv' % sys.argv[1], 'w')
print(outputFile)
exit()
writer = csv.writer(outputFile)
# write the header

writer.writerow(['postal', 'country', 'city', 'street', 'number', 'providers'])

with open('/Users/lsantos/Sites/personal/eend/split/output_%s.csv' % sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    # for loop but get the index of the row
    for row in reader:
        # get request to the api
        postal_code = row['Zipcode']
        # postal_code = '8011PK'

        data = requests.post('https://geo.api.mijnaansluiting.nl/api/%s/address' % postal_code)
        
        addresses = data.json()
        for address in addresses:
            address.pop('bagId')
            data = requests.post('https://geo.api.mijnaansluiting.nl/api/address/netbeheerderdiscipline', data=json.dumps(address), headers={'Content-Type': 'application/json'})
            # add data to the row['providers']
            # print(data.json())
            resp = data.json()
            # print(address)
            # exit()
            # if row['house_numbers'] == '':
            #     row.pop('house_numbers')
        
            row['providers'] = data.json()
            
            providerString = ''
            for provider in row['providers']:
                providerString += provider['netBeheerderCode'] + ' : ' + provider['disciplineCode'] + ' | '
            writer.writerow({
                'postal': address['postalCode'],
                'country': address['country'],
                'city': address['city'],
                'street': address['street'],
                'number': address['number'],
                'providers': providerString
            }.values())
outputFile.close()