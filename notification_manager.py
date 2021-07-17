from twilio.rest import Client
import os
import requests
from flight_search import FlightSearch
from data_manager import DataManager

class NotificationManager:
    def __init__(self):
        self.locations = ['LAX', 'JFK', 'HND']
        twilio_api_id = os.environ.get("twilio_id")
        twilio_auth_tok = os.environ.get("twilio_key")
        self.client = Client(twilio_api_id, twilio_auth_tok)
        self.bitly_pass = os.environ.get('bitly_key')
        self.search = FlightSearch(self.locations)
        dm = DataManager()
        self.location_price_df = dm.return_df()



    def link_shortener(self, link):
        return requests.post(url='https://api-ssl.bitly.com/v4/shorten',
                             headers={'Authorization': f'Bearer {self.bitly_pass}',
                                      'Content-Type': 'application/json'},
                             json={
                                 "long_url": link
                             }).json()['link']

    def text_creator(self):
        iteration = 0
        for item in self.search.get_list():

            temp_string = item['data'][0]['deep_link']
            temp = f"Flight to: {item['data'][0]['cityTo']}\n" \
                   f"Price of flight: {item['data'][0]['price']}$\n" \
                   f"Link: {self.link_shortener(link=temp_string)}\n\n"
            if item['data'][0]['price'] < self.location_price_df['Price'][iteration]:
                try:
                    twilio_string += temp
                except NameError:
                    twilio_string = temp
            iteration += 1
        return twilio_string

    def send_message(self, message, phones):
        self.client.messages \
            .create(
            body=message,
            from_='+18312222233',
            to=phones
        )
