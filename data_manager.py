import pandas
import os
import requests


class DataManager:
    def __init__(self):
        self.df_location = pandas.read_csv('location.csv')
        self.header = {'Authorization': os.environ.get('sheety_key')}
        r = requests.get(url='https://api.sheety.co/cb355fa7dfbe807c46143010b5acc159/flightContacts/sheet1',
                         headers=self.header)
        self.df_contacts = pandas.DataFrame.from_dict(r.json()['sheet1'])

    def return_df(self):
        return self.df_location

    def get_contacts(self):
        return self.df_contacts
