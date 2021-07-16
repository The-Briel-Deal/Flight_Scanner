# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import os
import json
import datetime
import flight_search

locations = ['LAX', 'JFK']
searchy = flight_search.FlightSearch(locations)

print(searchy.get_list())