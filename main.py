from data import Params
from api import FlightSearch

# Initialize parameters
params = Params()

# Create FlightSearch instance
flight_search = FlightSearch(params)

# Search for flights within budget and send notifications
flight_search.find_flights_within_budget()