import os
import requests
from dotenv import load_dotenv


class Params:
    def __init__(self):
        load_dotenv()

        # API URLs
        self.AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        # Amadeus API Configuration
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.token = self.get_access_token()

        # Twilio Configuration
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE")
        self.user_phone = os.getenv("USER_PHONE")

        # Destinations and maximum prices configuration
        self.destinations = {
            "LHR": 500,
            "CDG": 450,
            "MAD": 400,
            "BKK": 600,
        }

        # Departure airport
        self.origin = "JFK"

        # Travel dates
        self.dates = {
            "2025-06-15": "2025-06-25",
        }

#-----------------------------------------------------------------------------------------------------------------------
    def get_access_token(self):
        """Gets an access token from the Amadeus API."""
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(self.AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")
