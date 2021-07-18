from twilio.rest import Client
import os
import requests
from flight_search import FlightSearch
from data_manager import DataManager
import smtplib
import email.message


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
        self.contacts_df = dm.get_contacts()

        my_email = "gfapsnmpblasterbussy@gmail.com"
        password = "Doudles44%%"
        self.connection = smtplib.SMTP("smtp.gmail.com")
        self.connection.starttls()
        self.connection.login(user=my_email, password=password)

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
        self.email_clients(message)

    def email_clients(self, message):
        dict_email_clients = self.contacts_df.to_dict('records')
        for num in range(len(dict_email_clients)):
            firstname = dict_email_clients[num]['firstname']
            lastname = dict_email_clients[num]['lastname']
            email_address = dict_email_clients[num]['email']
            print(f'Your first name is {firstname}, Your last name is {lastname}, Your email is {email_address}')

            MESSAGE = email.message.EmailMessage()
            MESSAGE['Subject'] = f'Flights for {firstname} {lastname}'
            MESSAGE['From'] = 'gfapsnmpblasterbussy@gmail.com'
            MESSAGE['To'] = email_address
            MESSAGE.set_content(message)
            self.connection.send_message(MESSAGE)
