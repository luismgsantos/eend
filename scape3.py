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
import json
import sys
import requests
from pathlib import Path

def fetch_address_data(postal_code, session):
    """
    Fetch address data for a given postal code.
    """
    try:
        response = session.post(f'https://geo.api.mijnaansluiting.nl/api/{postal_code}/address')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching address data for postal code {postal_code}: {e}")
        return []

def fetch_providers(address, session):
    """
    Fetch provider data for a given address.
    """
    try:
        response = session.post(
            'https://geo.api.mijnaansluiting.nl/api/address/netbeheerderdiscipline',
            data=json.dumps(address),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching providers for address {address}: {e}")
        return []

def process_csv(file_id):
    """
    Process the CSV file for the given file_id.
    """
    # Use relative paths based on the script's location
    base_path = Path(__file__).resolve().parent
    input_file_path = base_path / 'split' / f'output_{file_id}.csv'
    output_file_path = base_path / 'done' / f'{file_id}.csv'

    try:
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
            reader = csv.DictReader(input_file)
            writer = csv.writer(output_file)
            writer.writerow(['postal', 'country', 'city', 'street', 'number', 'providers'])

            with requests.Session() as session:  # Use a session for connection reuse
                for row in reader:
                    postal_code = row.get('Zipcode', '').strip()
                    if not postal_code:
                        continue

                    addresses = fetch_address_data(postal_code, session)
                    for address in addresses:
                        address.pop('bagId', None)
                        providers = fetch_providers(address, session)
                        
                        # Prepare the provider string
                        provider_string = ' | '.join(
                            f"{provider['netBeheerderCode']} : {provider['disciplineCode']}"
                            for provider in providers
                        )

                        writer.writerow([
                            address.get('postalCode', ''),
                            address.get('country', ''),
                            address.get('city', ''),
                            address.get('street', ''),
                            address.get('number', ''),
                            provider_string
                        ])
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scape3.py <file_id>")
        sys.exit(1)

    file_id = sys.argv[1]
    process_csv(file_id)