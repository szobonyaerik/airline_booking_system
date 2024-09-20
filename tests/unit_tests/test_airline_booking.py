import pytest
from datetime import datetime
from airline_booking import Booking


@pytest.fixture
def booking():
    return Booking(
        name="Alice",
        departure_time=datetime(2024, 9, 19, 6, 45),
        itinerary=["LHR", "AMS"]
    )


def test_valid_booking_creation(booking):
    assert booking.name == "Alice"
    assert booking.departure_time == datetime(2024, 9, 19, 6, 45)
    assert booking.itinerary == ["LHR", "AMS"]


def test_name_empty():
    with pytest.raises(ValueError, match="Passenger name cannot be empty!"):
        Booking("", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])


def test_empty_itinerary():
    with pytest.raises(ValueError, match="Itinerary must be a non-empty list of valid IATA codes"):
        Booking("Alice", datetime(2024, 9, 19, 6, 45), [])


def test_invalid_itinerary_wrong_format():
    with pytest.raises(ValueError,
                       match="Itinerary must be a non-empty list of valid IATA codes, 3 letter strings, e.g., 'JFK', 'LHR'."):
        Booking("Alice", datetime(2024, 9, 19, 6, 45), ["AMS", "LHRH"])


def test_invalid_itinerary_with_invalid_characters():
    with pytest.raises(ValueError, match="Itinerary must be a non-empty list of valid IATA codes"):
        Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LH1", "AMS", "JFK"])


def test_invalid_itinerary_consecutive():
    with pytest.raises(ValueError, match="Consecutive duplicate airports are not allowed in the itinerary."):
        Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "LHR"])


def test_invalid_datetime():
    with pytest.raises(TypeError, match="departure_time must be a datetime object!"):
        Booking("Alice", '2024, 9, 19, 6, 45', ["LHR", "LHR"])
