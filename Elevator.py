"""Elevator class definition
This module defines an abstract base class for an Elevator system.
"""

import time
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import heapq


class State(Enum):
    """State enumeration for elevator states

    Attributes:
        IDLE: Elevator is not moving
        MOVING: Elevator is in motion
        DOOR_OPEN: Elevator door is open
        DOOR_CLOSED: Elevator door is closed
    """
    IDLE = 1
    UP = 2
    DOWN = 3
    EMERGENCY = 4


class ElevatorType(Enum):
    """ElevatorType enumeration for different types of elevators

    Attributes:
        PASSENGER: Passenger elevator
        FREIGHT: Freight elevator
        SERVICE: Service elevator
    """
    PASSENGER = 1
    FREIGHT = 2
    SERVICE = 3


class RequestOrigin(Enum):
    """RequestOrigin enumeration for the origin of elevator requests

    Attributes:
        BUTTON: Request from an elevator button
        CALL: Request from a call button outside the elevator
        SYSTEM: Request from the building management system
    """
    BUTTON = 1
    CALL = 2
    SYSTEM = 3


class DoorState(Enum):
    """DoorState enumeration for elevator door states

    Attributes:
        OPEN: Door is open
        CLOSED: Door is closed
        JAMMED: Door is jammed and cannot operate
    """
    OPEN = 1
    CLOSED = 2
    JAMMED = 3


class Elevator(ABC):
    """Elevator class definition

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, id: int, current_floor: int = 0):
        """_summary_

        Args:
            id (int): _description_
            current_floor (int, optional): _description_. Defaults to 0.
        """
        self.id = id
        self.current_floor = current_floor

    @abstractmethod
    def move(self, floor: int) -> None:
        """_summary_

        Args:
            floor (int): _description_
        """
        pass

    @abstractmethod
    def open_door(self) -> None:
        """_summary_
        """
        pass

    @abstractmethod
    def close_door(self) -> None:
        """_summary_
        """
        pass


class Request:
    """Request class definition

    Args:
        origin (RequestOrigin): The origin of the request
        origin_floor (int): The floor from which the request originated
        target_floor (int): The target floor for the request
    """

    def __init__(self, origin: RequestOrigin, origin_floor: int, target_floor: int | None = None):
        self.origin = origin
        self.direction = State.IDLE
        self.origin_floor = origin_floor
        self.target_floor = target_floor
        self.elevator_type = ElevatorType.PASSENGER
        self.door_state = DoorState.CLOSED
        self.request_time = datetime.now()

        if target_floor is not None:
            if target_floor > origin_floor:
                self.direction = State.UP
            elif target_floor < origin_floor:
                self.direction = State.DOWN
            else:
                self.direction = State.IDLE

    @property
    def origin_floor(self) -> int:
        """Get the origin floor of the request

        Returns:
            int: The origin floor
        """
        return self.origin_floor

    @origin_floor.setter
    def origin_floor(self, value: int) -> None:
        """Set the origin floor of the request

        Args:
            value (int): The new origin floor
        """
        if not isinstance(value, int):
            raise ValueError("Origin floor must be an integer.")
        self.origin_floor = value

    @property
    def target_floor(self) -> int | None:
        """Get the target floor of the request

        Returns:
            int | None: The target floor or None if not set
        """
        return self.target_floor

    @target_floor.setter
    def target_floor(self, value: int | None) -> None:
        """Set the target floor of the request

        Args:
            value (int | None): The new target floor or None
        """
        if value is not None and not isinstance(value, int):
            raise ValueError("Target floor must be an integer or None.")
        self.target_floor = value

    def __lt__(self, other: 'Request') -> bool:
        """Compare requests based on their origin floor

        Args:
            other (Request): The other request to compare with

        Returns:
            bool: True if this request's origin floor is less than the other's
        """
        return self.target_floor < other.target_floor


class ServiceRequest(Request):
    """ServiceRequest class definition, inheriting from Request

    Args:
        Request (_type_): _description_
    """

    def __init__(self, origin: RequestOrigin, origin_floor: int, target_floor: int | None = None):
        if origin_floor is None and target_floor is None:
            super().__init__(origin, origin_floor, target_floor)
        else:
            super().__init__(origin, origin_floor)
        self.elevator_type = ElevatorType.SERVICE
        self.door_state = DoorState.CLOSED


class Elevator:
    """Elevator class definition

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, id: int, emergency_status, current_floor: int = 0):
        """_summary_

        Args:
            id (int): _description_
            current_floor (int, optional): _description_. Defaults to 0.
        """
        self.id = id
        self.state = State.IDLE
        self.emergency_status = emergency_status
        self.current_floor = current_floor
        self.door_state = DoorState.CLOSED

    def open_door(self):
        """Open the elevator door"""
        if self.state == State.IDLE:
            self.door_state = DoorState.OPEN
            print(f"Elevator {self.id} door opened.")
        else:
            print(f"Cannot open door while elevator {self.id} is moving.")

    def close_door(self):
        """Close the elevator door"""
        if self.state == State.IDLE:
            self.door_state = DoorState.CLOSED
            print(f"Elevator {self.id} door closed.")
        else:
            print(f"Cannot close door while elevator {self.id} is moving.")

    def wait_for_seconds(self, seconds: int):
        """Wait for a specified number of seconds

        Args:
            seconds (int): Number of seconds to wait
        """
        print(f"Elevator {self.id} waiting for {seconds} seconds.")
        time.sleep(seconds)

    def operate(self):
        """Operate the elevator"""
        print(f"Elevator {self.id} is now in operation.")

    def process_emergency(self):
        """Handle emergency situations"""
        if self.emergency_status:
            self.state = State.EMERGENCY
            print(f"Elevator {self.id} is in emergency mode.")
        else:
            self.state = State.IDLE
            print(f"Elevator {self.id} is back to normal operation.")

    @property
    def current_floor(self) -> int:
        """Get the current floor of the elevator

        Returns:
            int: The current floor
        """
        return self._current_floor

    @current_floor.setter
    def current_floor(self, value: int) -> None:
        """Set the current floor of the elevator

        Args:
            value (int): The new current floor
        """
        if not isinstance(value, int):
            raise ValueError("Current floor must be an integer.")
        self._current_floor = value
        print(f"Elevator {self.id} is now on floor {self._current_floor}.")

    @property
    def state(self) -> State:
        """Get the current state of the elevator

        Returns:
            State: The current state of the elevator
        """
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        """Set the current state of the elevator

        Args:
            value (State): The new state of the elevator
        """
        if not isinstance(value, State):
            raise ValueError("State must be an instance of State Enum.")
        self._state = value
        print(f"Elevator {self.id} state changed to {self._state.name}.")

    @property
    def door_state(self) -> DoorState:
        """Get the current door state of the elevator

        Returns:
            DoorState: The current door state of the elevator
        """
        return self._door_state

    @door_state.setter
    def door_state(self, value: DoorState) -> None:
        """Set the current door state of the elevator

        Args:
            value (DoorState): The new door state of the elevator
        """
        if not isinstance(value, DoorState):
            raise ValueError(
                "Door state must be an instance of DoorState Enum.")
        self._door_state = value
        print(
            f"Elevator {self.id} door state changed to {self._door_state.name}.")

    @property
    def emergency_status(self) -> bool:
        """Get the emergency status of the elevator

        Returns:
            bool: True if in emergency mode, False otherwise
        """
        return self._emergency_status

    @emergency_status.setter
    def emergency_status(self, value: bool) -> None:
        """Set the emergency status of the elevator

        Args:
            value (bool): True to set emergency mode, False to clear it
        """
        if not isinstance(value, bool):
            raise ValueError("Emergency status must be a boolean.")
        self._emergency_status = value
        print(
            f"Elevator {self.id} emergency status set to {self._emergency_status}.")


class PassengerElevator(Elevator):
    """PassengerElevator class definition, inheriting from Elevator

    Args:
        Elevator (_type_): _description_
    """

    def __init__(self, id: int, emergency_status: bool, current_floor: int = 0):
        """_summary_

        Args:
            id (int): _description_
            emergency_status (bool): _description_
            current_floor (int, optional): _description_. Defaults to 0.
        """
        super().__init__(id, emergency_status, current_floor)
        self.passenger_up_queue = []
        self.passenger_down_queue = []
        self.elevator_type = ElevatorType.PASSENGER

    def operate(self):
        while self.passenger_down_queue or self.passenger_up_queue:
            self.process_requests()
        self.state = State.IDLE
        print(f"Elevator {self.id} has completed all requests.", self.state)

    def process_emergency(self):
        self.passenger_down_queue.clear()
        self.passenger_up_queue.clear()
        self.current_floor = 1
        self.door_state = DoorState.CLOSED
        self.state = State.IDLE
        self.emergency_status = True
        print(
            f"Queueus cleared, current floor is {self.current_floor}. Elevator {self.id} is processing emergency. Doors are {self.door_state.name}.")

    def add_up_request(self, request: Request):
        """Add a request to the passenger up queue

        Args:
            request (Request): The request to add
        """
        if not isinstance(request, Request):
            raise ValueError("Request must be an instance of Request.")
        if request.origin == RequestOrigin.CALL:
            pick_up_request = Request(
                request.origin, request.origin_floor, request.origin_floor)
            heapq.heappush(self.passenger_up_queue, pick_up_request)
        heapq.heappush(self.passenger_up_queue, request)
        print(
            f"Added up request from floor {request.origin_floor} to {request.target_floor}.")

    def add_down_request(self, request: Request):
        """Add a request to the passenger down queue

        Args:
            request (Request): The request to add
        """
        if not isinstance(request, Request):
            raise ValueError("Request must be an instance of Request.")
        if request.origin == RequestOrigin.CALL:
            drop_off_request = Request(
                request.origin, request.target_floor, request.target_floor)
            heapq.heappush(self.passenger_down_queue, drop_off_request)
        heapq.heappush(self.passenger_down_queue, request)
        print(
            f"Added down request from floor {request.origin_floor} to {request.target_floor}.")

    def process_up_requests(self):
        """Process the requests in the passenger queues"""
        while self.passenger_up_queue:
            up_request = heapq.heappop(self.passenger_up_queue)
            if self.current_floor == up_request.current_floor:
                print(
                    f"Current on floor {self.current_floor}. No movement as destination is the same.")
                continue
            print(
                f"The currrent floor is {self.current_floor}. Next stop: {up_request.target_floor}.")

            try:
                print(
                    f"Moving elevator {self.id} to floor {up_request.target_floor}.")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)
                time.sleep(1)
                print()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(f"Error moving elevator {self.id}: {e}")
                continue

            self.current_floor = up_request.target_floor
            print(f"Elevator {self.id} arrived at floor {self.current_floor}.")

            self.open_door()
            self.wait_for_seconds(3)
            self.close_door()
