from Room import Room

if __name__ == "__main__":
    room1 = Room(room_id=1, room_name="Study Room A", room_type="English Corridor", capacity=30, floor=1, permission="all")
    print(room1)

    # reservation test
    print("Booking slots...")
    print(f"Booking Day 0, TimeIndex 5: {room1.book_slot(day=0, time_index=5)}")
    print(room1)
    print(f"Booking Day 1, TimeIndex 3: {room1.book_slot(day=1, time_index=3)}")
    print(room1)
    print(f"Booking Day 1, TimeIndex 3 again (should fail): {room1.book_slot(day=1, time_index=3)}")

    # check the availability
    print("Checking availability...")
    print(f"Is Day 0, TimeIndex 5 available? {room1.is_available(day=0, time_index=5)}")
    print(f"Is Day 1, TimeIndex 3 available? {room1.is_available(day=1, time_index=3)}")
    print(f"Is Day 2, TimeIndex 4 available? {room1.is_available(day=2, time_index=4)}")

    # cancel the reservation
    print("Cancelling bookings...")
    print(f"Cancel Booking Day 0, TimeIndex 5: {room1.cancel_booking(day=0, time_index=5)}")
    print(f"Cancel Booking Day 1, TimeIndex 3: {room1.cancel_booking(day=1, time_index=3)}")
    print(f"Cancel Booking Day 1, TimeIndex 3 again (should fail): {room1.cancel_booking(day=1, time_index=3)}")

    # add equipment
    print("Adding equipment...")
    room1.add_equipment("Projector")
    room1.add_equipment("Whiteboard")
    room1.add_equipment("Projector")
    print(f"Current Equipment: {room1.equipment}")

    # remove equipment
    print("Removing equipment...")
    room1.remove_equipment("Whiteboard")
    room1.remove_equipment("TV")
    print(f"Current Equipment: {room1.equipment}")
