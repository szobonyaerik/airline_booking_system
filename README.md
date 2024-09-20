# Overview

This project simulates an airline booking system, managing bookings with features to search by departure time and airport routes. It ensures no duplicate bookings are added and maintains an efficient, sorted booking list.

## Key Features

- Add Bookings
- Store bookings with passenger names, departure times, and itineraries of IATA airport codes.
- Search Bookings: Search by departure time or find bookings with specific origin and destination airports.
- Prevent Duplicates: Ensure that duplicate bookings (same name, time, and itinerary) are not added.

## Assumptions
- IATA Codes: Airport codes are assumed to be valid 3-letter IATA codes.
- Datetime Format: Departure times are represented by Python datetime objects.
- Time Zones: The system does not handle time zones explicitly; times are assumed to be in the local time zone of the airport. Future improvements could include time zone support for cross-timezone flights.
- Duplicates: Identical bookings (name, time, itinerary) are considered duplicates.

## Tests
### Unit tests are provided to validate core features, including:

- Adding valid bookings.
- Preventing duplicates.
- Searching bookings by time and route.
- Handling invalid inputs gracefully.
