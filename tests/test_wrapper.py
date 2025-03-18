import time
import pytest
import why_too_fast_event_bus as wtf


# Test event subscription and publishing
def test_event_subscription_and_publish():
    bus = wtf.WhyTooFastEventBus()

    # Function to capture events
    captured_event = []

    def callback(data):
        captured_event.append(data)

    # Subscribe to the event in the "sistema" category
    bus.subscribe("system", "log_event", callback)

    # Publish event
    bus.publish("system", "log_event", {"message": "System started"})
    
    time.sleep(0.0001)

    # Verify the event was captured
    assert captured_event == [{"message": "System started"}]

def test_multiple_categories():
    bus = wtf.WhyTooFastEventBus()

    # Callback function for each category
    captured_system = []
    captured_notifications = []

    def system_callback(data):
        captured_system.append(data)

    def notifications_callback(data):
        captured_notifications.append(data)

    # Subscribe to events in different categories
    bus.subscribe("system", "log_event", system_callback)
    bus.subscribe("notifications", "email_event", notifications_callback)

    # Publish events in categories
    bus.publish("system", "log_event", {"message": "System started"})
    bus.publish("notifications", "email_event", {"email": "user@example.com"})
    
    time.sleep(0.0001)

    # Verify the events were captured correctly
    assert captured_system == [{"message": "System started"}]
    assert captured_notifications == [{"email": "user@example.com"}]

def test_multiple_instances_sharing_state():
    # Tests if two instances share the same state
    bus1 = wtf.WhyTooFastEventBus()
    bus2 = wtf.WhyTooFastEventBus()

    captured_event = []

    def callback(data):
        captured_event.append(data)

    # Subscribe to the event using the first instance
    bus1.subscribe("system", "log_event", callback)

    # Publish event using the second instance
    bus2.publish("system", "log_event", {"message": "System started via bus2"})
    
    time.sleep(0.0001)

    # Verify if the event was captured even though using the second instance
    assert captured_event == [{"message": "System started via bus2"}]

def test_different_event_categories():
    bus = wtf.WhyTooFastEventBus()

    captured_system = []
    captured_notifications = []

    def system_callback(data):
        captured_system.append(data)

    def notifications_callback(data):
        captured_notifications.append(data)

    # Subscribe to events
    bus.subscribe("system", "log_event", system_callback)
    bus.subscribe("notifications", "email_event", notifications_callback)

    # Publish events in their respective categories
    bus.publish("system", "log_event", {"message": "System event"})
    bus.publish("notifications", "email_event", {"email": "user@example.com"})
    
    time.sleep(0.0001)

    # Verify if the events were captured correctly
    assert captured_system == [{"message": "System event"}]
    assert captured_notifications == [{"email": "user@example.com"}]


def test_stress():
    bus = wtf.WhyTooFastEventBus()

    captured_event = []

    def callback(data):
        captured_event.append(data)

    # Subscribe to the event
    bus.subscribe("system", "log_event", callback)

    # Publish 1000 events
    for i in range(1000):
        bus.publish("system", "log_event", {"message": f"Event {i}"})
    
    time.sleep(0.1)

    # Verify if all events were captured
    assert len(captured_event) == 1000
    
    
def test_order_of_execution():
    bus = wtf.WhyTooFastEventBus()

    captured_event = []

    def callback(data):
        captured_event.append(data)

    # Subscribe to the event
    bus.subscribe("system", "log_event", callback)

    # Publish 1000 events
    for i in range(1000):
        bus.publish("system", "log_event", {"message": f"Event {i}"})
        
    time.sleep(0.0001)

    # Verify if the events were captured in the correct order
    for i, event in enumerate(captured_event):
        assert event["message"] == f"Event {i}"