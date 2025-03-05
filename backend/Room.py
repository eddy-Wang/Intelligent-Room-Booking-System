class Room:
    def __init__(self, room_id, room_name, room_type, capacity, floor, permission):
        """
        Initialize the room with basic information.
        :param room_id: Unique identifier for the room.
        :param room_name: Name of the room.
        :param room_type: Type of the room (e.g. "English Corridor rooms").
        :param capacity: Maximum number of people the room can accommodate.
        :param floor: Floor number where the room is located.
        :param permission: Access permission for the room (e.g."staff only").
        """
        self.room_id = room_id
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity
        self.floor = floor
        self.permission = permission  # Permission for access control
        self.equipment = []  # List to store room equipment information.
        self.schedule = self._initialize_schedule()

    def _initialize_schedule(self):
        """
        Initialize the booking schedule for the room with 10 fixed time slots.
        """
        return [[0 for _ in range(12)] for _ in range(7)]  # 7 days, 10 time slots per day

    def is_available(self, day, time_index):
        """
        Check if a specific time slot is available for booking.
        :param day: Day of the week (0-6, where 0 is Monday and 6 is Sunday).
        :param time_index: Index of the time slot (0 to total number of slots - 1).
        :return: True if the slot is available, False otherwise.
        """
        return self.schedule[day][time_index] == 0

    def book_slot(self, day, time_index):
        """
        Book a specific time slot.
        :param day: Day of the week (0-6, where 0 is Monday and 6 is Sunday).
        :param time_index: Index of the time slot (0 to total number of slots - 1).
        :return: True if the booking is successful, False otherwise.
        """
        if self.is_available(day, time_index):
            self.schedule[day][time_index] = 1
            return True
        return False

    def cancel_booking(self, day, time_index):
        """
        Cancel a booking for a specific time slot.
        :param day: Day of the week (0-6, where 0 is Monday and 6 is Sunday).
        :param time_index: Index of the time slot (0 to total number of slots - 1).
        :return: True if the cancellation is successful, False otherwise.
        """
        if self.schedule[day][time_index] == 1:
            self.schedule[day][time_index] = 0
            return True
        return False

    def add_equipment(self, equipment):
        """
        Add equipment to the room.
        :param equipment: Name of the equipment to add.
        """
        if equipment not in self.equipment:
            self.equipment.append(equipment)
            print(f"Equipment '{equipment}' added to Room {self.room_id}.")
        else:
            print(f"Equipment '{equipment}' already exists in Room {self.room_id}.")

    def remove_equipment(self, equipment):
        """
        Remove equipment from the room.
        :param equipment: Name of the equipment to remove.
        """
        if equipment in self.equipment:
            self.equipment.remove(equipment)
            print(f"Equipment '{equipment}' removed from Room {self.room_id}.")
        else:
            print(f"Equipment '{equipment}' not found in Room {self.room_id}.")

    def get_schedule(self):
        """
        Get the current booking schedule for the room.
        :return: A 2D array representing the booking schedule.
        """
        return self.schedule

    def set_permission(self, permission):
        """
        Set the permission level for the room.
        :param permission: New permission.
        """
        self.permission = permission
        print(f"Permission level for Room {self.room_id} set to '{permission}'.")

    def check_permission(self, user_role):
        """
        Check if a user with a specific role has permission to access the room.
        :param user_role: Role of the user
        :return: True if the user has permission, False otherwise.
        """
        if self.permission == "all":
            return True
        elif self.permission == "all staff" and user_role in ["all staff", "certain staff"]:
            return True
        elif self.permission == "certain staff":
            # TODO
            return True
        return False

    def __str__(self):
        """
        Return a string representation of the room information.
        """
        return (f"Room ID: {self.room_id}\n"
                f"Room Name: {self.room_name}\n"
                f"Room Type: {self.room_type}\n"
                f"Capacity: {self.capacity}\n"
                f"Floor: {self.floor}\n"
                f"Permission: {self.permission}\n"
                f"Equipment: {', '.join(self.equipment) if self.equipment else 'None'}\n"
                f"Schedule: {self.schedule}")