import argparse
import configparser
import logging

from icalendar import Calendar
import recurring_ical_events
import x_wr_timezone

_DEFAULT_DATA_DIR = "data"
_CONFIG_FILE = "config.ini"

_config_parser = None
_console_log_level = logging.INFO
_logfile_log_level = logging.INFO
_logfile_name = "parse_calendar.log"
_logger = logging.getLogger(__name__)


def load_config_file() -> None:
    global _config_parser
    _config_parser = configparser.ConfigParser()
    _config_parser.read(_CONFIG_FILE)
    # set variables from config
    if "logging" in _config_parser:
        logging_config = _config_parser["logging"]
        _console_log_level = logging_config.get("console_log_level", _console_log_level)
        _logfile_log_level = logging_config.get("logfile_log_level", _logfile_log_level)
        _logfile_name = logging_config.get("logfile_name", _logfile_name)


def update_config_file() -> None:
    global _config_parser
    # if this is called before load_config_file, assume we are creating a config file?
    # if that doesn't make sense, then this should be an exception instead
    if not _config_parser:
        _config_parser = configparser.ConfigParser()
        # raise RuntimeError("update_config_file called before load_config_file")
    # config_parser['Login Parameters']['refresh_token'] = token_dict['refresh_token']
    with open(_CONFIG_FILE, "w") as configfile:
        _config_parser.write(configfile)


def initialize_logging() -> None:
    _logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(name)s - %(asctime)s (%(levelname)s): %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S %z"
    ch = logging.StreamHandler()
    ch.setLevel(_console_log_level)
    ch.setFormatter(formatter)
    _logger.addHandler(ch)
    fh = logging.FileHandler(_logfile_name)
    fh.setLevel(_logfile_log_level)
    fh.setFormatter(formatter)
    _logger.addHandler(fh)


def main() -> None:
    start_date = (2023, 1, 1)
    end_date = (2023, 1, 31)

    with open("distrokid.ics", "rb") as file:
        calendar = Calendar.from_ical(file.read())
    new_calendar = x_wr_timezone.to_standard(calendar)
    events = recurring_ical_events.of(new_calendar).between(start_date, end_date)

    for event in events:
        print(event["summary"])
        print(f"\t{event['dtstart'].dt} - {event['dtend'].dt}")
        if "description" in event:
            print("\t" + event["description"])
        print(f"\ttimestamp:{event['dtstamp'].dt}")
        if "attendee" in event:
            for attendee in event["attendee"]:
                print(f"\tattendee: {attendee}")
        if "organizer" in event:
            print(f"\torganizer: {event['organizer']}")
        print(f"\t{event['status']}")

    """
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
    """


# when run as a script, do initialization
if __name__ == "__main__":
    load_config_file()

    # command-line arguments override config file settings
    parser = argparse.ArgumentParser(
        description="Convert calendar file into json event and people list."
    )
    parser.add_argument("--verbose", "-v", action="store_true", dest="verbose")
    parser.add_argument("--verbose_log", "-V", action="store_true", dest="verbose_log")
    ns = parser.parse_args()
    if ns.verbose:
        _console_log_level = logging.DEBUG
    if ns.verbose_log:
        _logfile_log_level = logging.DEBUG

    initialize_logging()
    main()
