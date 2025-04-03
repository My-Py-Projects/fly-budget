import requests
import urllib.parse
from twilio.rest import Client
from data import Params


class FlightSearch:
    def __init__(self, params):
        """Initializes the class with parameters and credentials."""
        self.params = params
        self.token = params.token
        self.flight_search_url = params.FLIGHT_SEARCH_URL

    # -----------------------------------------------------------------------------------------------------------------#
    def search_flights(self, origin, destination, departure_date, return_date):
        """Searches for flights to a specific destination and date."""
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "currencyCode": "USD",
            "max": 5
        }
        response = requests.get(self.flight_search_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    # -----------------------------------------------------------------------------------------------------------------#
    def generate_google_search_link(self, origin, destination, departure_date, return_date):
        """Generates a Google search link for booking flights."""
        base_url = "https://www.google.com/search?"
        query = f"flights from {origin} to {destination} on {departure_date} returning {return_date}"
        return base_url + urllib.parse.urlencode({"q": query})

    # -----------------------------------------------------------------------------------------------------------------#
    def filter_flights(self, data, max_price):
        """Filters flights below the maximum price and generates a booking link."""
        if not data or "data" not in data or not data["data"]:
            return None

        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])
            if price <= max_price:
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                departure_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
                booking_url = self.generate_google_search_link(origin, destination, departure_date, return_date)

                return {
                    "price": price,
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "booking_url": booking_url
                }
        return None

    # -----------------------------------------------------------------------------------------------------------------#
    def get_flight_below_price(self, destination, departure, return_date, max_price):
        """Checks if there is a flight below the maximum price for a destination and date."""
        response = self.search_flights(self.params.origin, destination, departure, return_date)
        return self.filter_flights(response, max_price)

    # -----------------------------------------------------------------------------------------------------------------#
    def find_flights_within_budget(self):
        """Returns all flights within the defined budget for each destination and sends an SMS alert."""
        flights_within_budget = []

        for dest, max_price in self.params.destinations.items():
            for dep, ret in self.params.dates.items():
                flight = self.get_flight_below_price(dest, dep, ret, max_price)

                if flight:
                    flights_within_budget.append(flight)
                    self.send_notification(flight)

        return flights_within_budget if flights_within_budget else None

    # -----------------------------------------------------------------------------------------------------------------------
    def send_notification(self, flight):
        """Sends an SMS notification with flight details."""
        client = Client(self.params.twilio_sid, self.params.twilio_auth_token)

        message_body = (
            f"✈️ Cheap Flight Alert! ✈️\n"
            f"From: {flight['origin']} → To: {flight['destination']}\n"
            f"Departure: {flight['departure_date']} | Return: {flight['return_date']}\n"
            f"Price: ${flight['price']}\n"
            f"🔗 Check it out: {flight['booking_url']}"
        )

        client.messages.create(
            body=message_body,
            from_=self.params.twilio_phone,
            to=self.params.user_phone
        )

    # -----------------------------------------------------------------------------------------------------------------------


# Run script
if __name__ == "__main__":
    params = Params()
    flight_search = FlightSearch(params)

    # Searches for all flights within the budget
    budget_flights = flight_search.find_flights_within_budget()