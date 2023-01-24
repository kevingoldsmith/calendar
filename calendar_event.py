"""
    class for an event on the calendar
"""
from typing import Dict


def _parse_person(event_person: str) -> str:
    """
    _parse_person given a string from an event, clean it up

    Args:
        event_person (str): the organizer or attendee

    Returns:
        str: a cleaned up string or an empty string if it can't be cleaned up
    """
    if event_person.startswith("mailto:"):
        email = event_person[7:]
        if email.endswith("calendar.google.com"):
            return ""
        return email
    return event_person


class CalendarEvent:
    """
    _summary_
    """

    def __init__(self, base_event: Dict) -> None:
        """
        __init__ initialize using a dictionary form recurring_ical_events

        Args:
            base_event (Dict): the expected format would be the return from
            recurring_ical_events
        """
        self.summary = base_event["summary"]
        self.start = base_event["dtstart"].dt
        self.end = base_event["dtend"].dt
        self.timestamp = base_event["dtstamp"].dt
        self.description = base_event.get("description", "")
        self.organizer = _parse_person(base_event.get("organizer", ""))
        self.attendees = []
        if "attendee" in base_event:
            for attendee in base_event["attendee"]:
                parsed = _parse_person(attendee)
                if parsed:
                    self.attendees.append(parsed)

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

    def dict_for_csv(self) -> dict:
        return_dict = {}
        return_dict["summary"] = str(self.summary)
        return_dict["start"] = str(self.start)
        return_dict["end"] = str(self.end)
        return_dict["timestamp"] = str(self.timestamp)
        return_dict["description"] = str(self.description)
        return_dict["organizer"] = self.organizer
        return_dict["attendees"] = ','.join(self.attendees)
        return return_dict
