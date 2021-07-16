import requests
import os
import json


class FlightSearch:
    def __init__(self, locations):
        api_key = os.environ.get('kiwi_key')

        self.flight_prices = []
        for location in locations:
            flight_price = requests.get(url='http://tequila-api.kiwi.com/v2/search',
                                        params={'fly_from': 'TPA',
                                                'date_from': '17/07/2021',
                                                'date_to': '17/07/2022',
                                                'fly_to': location,
                                                'one_for_city': '1'},
                                        headers={'apikey': api_key}
                                        )
            self.flight_prices.append(flight_price.json())

        with open('dog.json', mode='w') as dog:
            json.dump(self.flight_prices, fp=dog, indent=4)

    def get_list(self):
        return self.flight_prices
