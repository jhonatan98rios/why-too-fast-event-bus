import typing as typ
import why_too_fast_event_bus_module as wtf

class WhyTooFastEventBus:
    _shared_state = {}  # Shared state between instances

    def __init__(self):
        self.__dict__ = self._shared_state  # Share state between instances
        if not hasattr(self, "_event_buses"):
            self._event_buses = {}  # Dict to store event buses

    def _get_or_create_bus(self, category: str) -> wtf.WhyTooFastEventBus:
        """It returns the event bus for the given category, creating it if it doesn't exist."""
        if category not in self._event_buses:
            self._event_buses[category] = wtf.WhyTooFastEventBus()
        return self._event_buses[category]

    def subscribe(self, category: str, event: str, callback: typ.Callable[..., None]) -> None:
        """
        It subscribes a callback to an event within a specific category.

        Args:
            category (str): Name of the event bus category.
            event (str): Name of the event.
            callback (Callable): Callback function to be called when the event occurs.
        """
        self._get_or_create_bus(category).subscribe(event, callback)

    def publish(self, category: str, event: str, data: dict) -> None:
        """
        It publishes an event to the event bus.

        Args:
            category (str): Name of the event bus category.
            event (str): Name of the event.
            data (dict): Data to be passed to the callback functions.
        """
        self._get_or_create_bus(category).publish(event, data)
