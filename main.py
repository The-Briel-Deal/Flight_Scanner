import requests
import os
import json
import datetime

import data_manager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from data_manager import DataManager

# ----- DECLARING VARIABLES ----- #

my_phone = os.environ.get('my_phone')

# ----- INITIALIZING CLASSES ----- #

notification = NotificationManager()
text = notification.text_creator()
dm = data_manager.DataManager()

# ----- Twilio Testing----- #

notification.send_message(message=text, phones=my_phone)
