import pytest
from datetime import datetime
from airline_booking import Booking
from booking_system import BookingSystem


@pytest.fixture
def booking_system():
    return BookingSystem()


def test_add_booking_in_sorted_order(booking_system):
    """
    Ensure sorted list works as expected
    """
    booking1 = Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    booking2 = Booking("Bruce", datetime(2024, 9, 19, 18, 45), ["LHR", "AMS"])
    booking3 = Booking("Cindy", datetime(2024, 9, 18, 18, 30), ["JFK", "SFO"])
    booking_system.add_booking(booking2)
    booking_system.add_booking(booking1)
    booking_system.add_booking(booking3)

    assert booking_system.booking_list[0].name == "Cindy"
    assert booking_system.booking_list[1].name == "Alice"
    assert booking_system.booking_list[2].name == "Bruce"


def test_add_same_departure_time(booking_system):
    """
    Ensure both bookings are added,
    order may not be predictable for same time
    """
    booking1 = Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    booking2 = Booking("Bruce", datetime(2024, 9, 19, 6, 45), ["AMS", "LHR"])

    booking_system.add_booking(booking1)
    booking_system.add_booking(booking2)

    assert len(booking_system.booking_list) == 2
    # Order of bookings with the same departure time is not guaranteed
    assert booking_system.booking_list[0].departure_time == booking1.departure_time
    assert booking_system.booking_list[1].departure_time == booking2.departure_time


def test_add_invalid_booking_directly(booking_system):
    # Assuming an invalid booking could exist somehow
    with pytest.raises(TypeError):
        booking_system.add_booking("InvalidBookingObject")


def test_add_duplicate_bookings(booking_system):
    """
    Test that adding the same booking twice raises a ValueError.
    """
    booking = Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])

    booking_system.add_booking(booking)

    with pytest.raises(ValueError, match="This booking already exists in the system."):
        booking_system.add_booking(booking)


def test_create_and_add_single_booking(booking_system):
    """
    Test that a single booking is created and added to the system correctly
    using the create_and_add_booking() method.
    """
    booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])

    assert len(booking_system.booking_list) == 1
    booking = booking_system.booking_list[0]
    assert booking.name == "Alice"
    assert booking.departure_time == datetime(2024, 9, 19, 6, 45)
    assert booking.itinerary == ["LHR", "AMS"]


def test_create_and_add_multiple_booking_sorted(booking_system):
    """
    Ensure create_and_add_booking inserts multiple
    bookings into the sorted list.
    """
    booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    booking_system.create_and_add_booking("Bruce", datetime(2024, 9, 19, 18, 45), ["LHR", "AMS"])
    booking_system.create_and_add_booking("Cindy", datetime(2024, 9, 18, 18, 30), ["JFK", "SFO"])

    # Check if the bookings are sorted correctly by departure_time
    assert booking_system.booking_list[0].name == "Cindy"
    assert booking_system.booking_list[1].name == "Alice"
    assert booking_system.booking_list[2].name == "Bruce"


def test_create_and_add_booking_invalid_inputs(booking_system):
    """
    Test that create_and_add_booking() handles invalid inputs correctly by raising appropriate errors.
    """
    with pytest.raises(ValueError, match="Passenger name cannot be empty!"):
        booking_system.create_and_add_booking("", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])

    with pytest.raises(TypeError, match="departure_time must be a datetime object!"):
        booking_system.create_and_add_booking("Alice", "2024-09-19 06:45", ["LHR", "AMS"])

    with pytest.raises(ValueError, match="Itinerary must be a non-empty list of valid IATA codes"):
        booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), [])

    with pytest.raises(ValueError, match="Consecutive duplicate airports are not allowed in the itinerary."):
        booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "LHR"])


def test_create_and_add_already_existing_booking(booking_system):
    """
    Test that a single booking is created and added to the system correctly
    using the create_and_add_booking() method.
    """
    booking = Booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    booking_system.add_booking(booking)

    with pytest.raises(ValueError, match="This booking already exists in the system."):
        booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])


def test_search_before(booking_system):
    """
    Test that search_before returns the correct list of bookings departing before the target time.
    """
    booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    booking_system.create_and_add_booking("Bruce", datetime(2024, 9, 19, 9, 30), ["AMS", "LHR"])
    booking_system.create_and_add_booking("Cindy", datetime(2024, 9, 18, 18, 30), ["JFK", "SFO"])

    # Two results expected
    result = booking_system.search_before(datetime(2024, 9, 19, 8, 0))
    assert len(result) == 2
    assert result[0].name == "Cindy"
    assert result[1].name == "Alice"

    # One result expected
    result = booking_system.search_before(datetime(2024, 9, 18, 19, 0))
    assert len(result) == 1
    assert result[0].name == "Cindy"

    # No results expected
    result = booking_system.search_before(datetime(2024, 9, 18, 0, 0))
    assert len(result) == 0


def test_search_before_invalid_target_time(booking_system):
    """
    Test that search_before raises an error when the target_time is not a datetime object.
    """
    booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS"])
    with pytest.raises(TypeError, match="target_time must be a datetime object!"):
        booking_system.search_before("2024-09-19 06:45")


def test_search_route(booking_system):
    """
    Test that search_route correctly returns bookings where the itinerary passes
    through origin before destination.
    """
    booking_system.create_and_add_booking("Alice", datetime(2024, 9, 19, 6, 45), ["LHR", "AMS", "JFK"])
    booking_system.create_and_add_booking("Bruce", datetime(2024, 9, 19, 18, 45), ["AMS", "LHR", "JFK", "AMS"])
    booking_system.create_and_add_booking("Cindy", datetime(2024, 9, 18, 18, 30), ["LHR", "JFK", "AMS"])

    result = booking_system.search_route("LHR", "AMS")
    assert len(result) == 1
    assert result[0].name == "Alice"

    result = booking_system.search_route("JFK", "AMS")
    assert len(result) == 2
    assert result[0].name == "Cindy"
    assert result[1].name == "Bruce"

    result = booking_system.search_route("AMS", "GVA")
    assert len(result) == 0


def test_search_route_no_bookings(booking_system):
    """
    Test that search_route returns an empty list when there are no bookings in the system.
    """
    result = booking_system.search_route("LHR", "AMS")
    assert len(result) == 0


def test_search_route_invalid_origin_not_string(booking_system):
    """
    Test that search_route raises a TypeError when origin is not a string.
    """
    with pytest.raises(TypeError, match="Origin and destination must be strings."):
        booking_system.search_route(123, "AMS")


def test_search_route_invalid_destination_not_string(booking_system):
    """
    Test that search_route raises a TypeError when destination is not a string.
    """
    with pytest.raises(TypeError, match="Origin and destination must be strings."):
        booking_system.search_route("LHR", 123)


def test_search_route_invalid_origin_length(booking_system):
    """
    Test that search_route raises a ValueError when origin is not 3 letters.
    """
    with pytest.raises(ValueError,
                       match="Origin and destination must be valid 3-letter IATA airport codes, e.g., 'JFK', 'LHR'."):
        booking_system.search_route("LH", "AMS")


def test_search_route_invalid_destination_length(booking_system):
    """
    Test that search_route raises a ValueError when destination is not 3 letters.
    """
    with pytest.raises(ValueError,
                       match="Origin and destination must be valid 3-letter IATA airport codes, e.g., 'JFK', 'LHR'."):
        booking_system.search_route("LHR", "AMSA")


def test_search_route_same_origin_and_destination(booking_system):
    """
    Test that search_route raises a ValueError when origin and destination are the same.
    """
    with pytest.raises(ValueError, match="Origin and destination must be different."):
        booking_system.search_route("LHR", "LHR")
