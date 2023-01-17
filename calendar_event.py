"""
    class for an event on the calendar
"""
from typing import Dict

class CalendarEvent:
    """
     _summary_
    """

    def __init__(self, base_event:Dict) -> None:
        """
        __init__ initialize using a dictionary form recurring_ical_events

        Args:
            base_event (Dict): the expected format would be the return from
            recurring_ical_events
        """
        self.summary = base_event["summary"]
        self.start = base_event['dtstart'].dt
        self.end = base_event['dtend'].dt
        self.timestamp = base_event['dtstamp'].dt
        self.description = base_event.get('description', '')
        self.organizer = base_event.get('organizer', '')
        self.attendees = []
        if "attendee" in base_event:
            for attendee in base_event["attendee"]:
                self.attendees.append(attendee)

    def __str__(self) -> str:
        """
        __str__ get a string representation of the object

        Returns:
            str: a string representation of the object
        """
        return f"{self.summary}: {self.start} - {self.end}"

    def to_dict(self) -> dict:
        """
        to_dict get a dictionary representation of the object

        Returns:
            dict: the dictionary
        """
        return vars(self)
