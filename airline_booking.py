from datetime import datetime
import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Booking:
    def __init__(self, name: str, departure_time: datetime, itinerary: list):
        """
        A class to represent an airline booking.
        Initialize a booking with the passenger name, departure time, and itinerary.

        :param name: Name of the passenger.
        :param departure_time: A datetime object representing the departure time.
        :param itinerary: A list of airport codes, 3-letter strings, representing the route.
        """
        logging.info(f"Creating booking for {name} at {departure_time} with itinerary {itinerary}")

        if not name:
            logging.error("Passenger name is empty.")
            raise ValueError("Passenger name cannot be empty!")

        if not isinstance(departure_time, datetime):
            logging.error("Invalid departure_time: must be a datetime object.")
            raise TypeError("departure_time must be a datetime object!")

        if not itinerary or not all(isinstance(airport, str) and len(airport) == 3 and airport.isalpha() for airport in itinerary):
            logging.error("Invalid itinerary: must be a non-empty list of valid IATA codes, 3 letter strings.")
            raise ValueError("Itinerary must be a non-empty list of valid IATA codes, 3 letter strings, e.g., 'JFK', 'LHR'.")

        for i in range(1, len(itinerary)):
            if itinerary[i] == itinerary[i - 1]:
                logging.error("Invalid itinerary: consecutive duplicate airports.")
                raise ValueError("Consecutive duplicate airports are not allowed in the itinerary.")

        self.name = name
        self.departure_time = departure_time
        self.itinerary = itinerary
        logging.info(f"Booking for {name} successfully created.")

    def __repr__(self):
        itinerary_str = ' -> '.join(self.itinerary)
        return f"Booking({self.name}, {self.departure_time}, {itinerary_str})"
