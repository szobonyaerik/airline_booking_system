from bisect import bisect_left, insort
from datetime import datetime
import logging
import sys

from airline_booking import Booking


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class BookingSystem:
    """
    A class to represent a booking system of an airline.
    A system for managing airline bookings, allowing users to add bookings and perform
    searches based on departure time or specific routes (origin and destination airports).
    """
    def __init__(self):
        self.booking_list = []
        logging.info("BookingSystem initialized with an empty booking list.")

    def add_booking(self, booking: Booking):
        """
        Insert an already existing booking into the sorted list based on departure_time.
        """
        if not isinstance(booking, Booking):
            raise TypeError("booking must be an instance of the Booking class")

        # Check for exact duplicates
        for existing_booking in self.booking_list:
            if (existing_booking.name == booking.name and
                    existing_booking.departure_time == booking.departure_time and
                    existing_booking.itinerary == booking.itinerary):
                raise ValueError("This booking already exists in the system.")

        insort(self.booking_list, booking, key=lambda b: b.departure_time)
        logging.info(f"Booking for {booking.name} added successfully.")

    def create_and_add_booking(self, name: str, departure_time: datetime, itinerary: list):
        """
        Create a new Booking and automatically add it to the system.
        """
        booking = Booking(name, departure_time, itinerary)
        logging.info(f"Booking for {name} created successfully.")
        self.add_booking(booking)

    def search_before(self, target_time: datetime):
        """
        Return a list of bookings that have a departure_time before the target_time.
        """
        if not isinstance(target_time, datetime):
            logging.error("Invalid target_time for search_before: must be a datetime object.")
            raise TypeError("target_time must be a datetime object!")

        index = bisect_left(self.booking_list, target_time, key=lambda b: b.departure_time)
        logging.info(f"Found {index} bookings departing before {target_time}.")
        return self.booking_list[:index]

    def search_route(self, origin: str, destination: str):
        """
         Return a list of bookings where the itinerary passes through origin exactly before destination.
        """
        if not (isinstance(origin, str) and isinstance(destination, str)):
            logging.error("Invalid origin or destination: must be strings.")
            raise TypeError("Origin and destination must be strings.")

        if len(origin) != 3 or not origin.isalpha() or len(destination) != 3 or not destination.isalpha():
            logging.error(f"Invalid IATA codes for route search: origin={origin}, destination={destination}")
            raise ValueError("Origin and destination must be valid 3-letter IATA airport codes, e.g., 'JFK', 'LHR'.")

        if origin == destination:
            logging.error("Invalid route search: origin and destination are the same.")
            raise ValueError("Origin and destination must be different.")

        matching_bookings = []

        for booking in self.booking_list:
            itinerary = booking.itinerary
            for i in range(len(itinerary) - 1):
                if itinerary[i] == origin and itinerary[i + 1] == destination:
                    matching_bookings.append(booking)
                    break

        logging.info(f"Found {len(matching_bookings)} bookings with route {origin} -> {destination}.")
        return matching_bookings

    def __repr__(self):
        return f'BookingSystem({self.booking_list})'
