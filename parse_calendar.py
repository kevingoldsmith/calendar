from icalendar import Calendar
import x_wr_timezone
import recurring_ical_events


start_date = (2023, 1, 1)
end_date =   (2023, 1, 31)

with open("distrokid.ics", 'rb') as file:
    calendar = Calendar.from_ical(file.read())
new_calendar = x_wr_timezone.to_standard(calendar)
events = recurring_ical_events.of(new_calendar).between(start_date, end_date)

for component in new_calendar.walk():
    if component.name == "VEVENT":
        print(component.get('summary'))
        print(f"\t{component.get('dtstart').dt} - {component.get('dtend').dt}")
        print(component.get('description'))
        print(f"\ttimestamp:{component.get('dtstamp').dt}")
        if component.get('attendee'):
            for attendee in component.get('attendee'):
                print(f"\tattendee: {attendee}")
        print(f"\torganizer: {component.get('organizer')}")
        print(f"\t{component.get('status')}")

for event in events:
    print(event['summary'])
    print(f"\t{event['dtstart'].dt} - {event['dtend'].dt}")
    if 'description' in event:
        print('\t' + event['description'])
    print(f"\ttimestamp:{event['dtstamp'].dt}")
    if 'attendee' in event:
        for attendee in event['attendee']:
            print(f"\tattendee: {attendee}")
    if 'organizer' in event:
        print(f"\torganizer: {event['organizer']}")
    print(f"\t{event['status']}")
