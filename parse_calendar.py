"""parse a ical calendar file and produce a list of events and a people
"""

import argparse
import configparser
import csv
import logging
import os
from typing import Dict, Any, TextIO, List

from icalendar import Calendar  # type: ignore
import recurring_ical_events  # type: ignore
import x_wr_timezone  # type: ignore

from calendar_event import CalendarEvent
from contact import Contact
from contact_list import ContactList

_DEFAULT_DATA_DIR = "data"
_CONFIG_FILE = "parse_calendar.ini"
_LOG_FILE = "parse_calendar.log"
_CONSOLE_LEVEL = logging.INFO
_FILE_LEVEL = logging.INFO
_CONTACTS_FILE = _DEFAULT_DATA_DIR + "/" + "contacts.csv"

_logger = logging.getLogger(
    __name__ if __name__ != "__main__" else "parse_calendar"
)  # pylint: disable=C0103

_contact_list = ContactList()
_calendar_event_list = []


def load_config_file(base_config: dict) -> configparser.ConfigParser:
    """Load the configuration file and initialize any variables

    Args:
        base_config (dict): the default configuration values

    Returns:
        configparser.ConfigParser: the config_parser object in case you want to
        use it for saving the configuration
    """
    parser = configparser.ConfigParser()
    parser.read(_CONFIG_FILE)
    # set variables from config
    if "logging" in parser:
        logging_config = parser["logging"]
        base_config["console_log_level"] = int(
            logging_config.get(
                "console_log_level", str(base_config["console_log_level"])
            )
        )
        base_config["logfile_log_level"] = int(
            logging_config.get(
                "logfile_log_level", str(base_config["logfile_log_level"])
            )
        )
        base_config["logfile_name"] = logging_config.get(
            "logfile_name", base_config["logfile_name"]
        )

    if "contacts" in parser:
        contacts_config = parser["contacts"]
        base_config["contacts_file"] = contacts_config.get(
            "contacts_file", base_config["contacts_file"]
        )

    return parser


def update_config_file(parser: configparser.ConfigParser) -> None:
    """Save the configuration file. A later version of this should take in any
    non global variables as a parameter

    Args:
        parser (configparser.ConfigParser): the config parser object

    Raises:
        ValueError: if the parser is None
    """
    if not parser:
        raise ValueError("update_config_file called before load_config_file")
    # config_parser['Login Parameters']['refresh_token'] = token_dict['refresh_token']
    with open(_CONFIG_FILE, "w", encoding="UTF-8") as configfile:
        parser.write(configfile)


def initialize_logging(
    logfile_name: str, console_log_level: int, logfile_log_level: int
) -> None:
    """Initialize logging settings

    Args:
        logfile_name (str): the file name to save the file log to, use None to not save a log file
        console_log_level (int): the logging level for console log messages
        logfile_log_level (int): the logging level for file log messages
    """
    _logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(name)s - %(asctime)s (%(levelname)s): %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S %z"
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    if logfile_name:
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setLevel(logfile_log_level)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)


def initialize_contact_list(contact_file_path: str) -> None:
    """
    initialize_contact_list initialize the contact list with existing contacts

    Args:
        contact_file_path (str): filepath to the contacts file
    """
    if os.path.exists(contact_file_path):
        _contact_list.load_from_file(contact_file_path)
    else:
        _logger.debug("contact file does not exist: %s", contact_file_path)


def save_contact_list(contact_file_path: str) -> None:
    """
    save_contact_list save the contacts to a file to reference for next runs

    Args:
        contact_file_path (str): path to the destination file
    """
    if not os.path.exists(contact_file_path):
        dir_name = os.path.dirname(contact_file_path)
        os.makedirs(dir_name, exist_ok=True)
    _logger.debug("saving contacts list: %s", contact_file_path)
    _contact_list.save_to_file(contact_file_path)


def save_calendar_list(calendar_item_list:List[CalendarEvent]) -> None:
    cal_dict_list = []
    for cal_event in calendar_item_list:
        cal_dict_list.append(cal_event.dict_for_csv())
    with open("cal.csv", "w", encoding="utf-8") as file:
        csvwriter = csv.DictWriter(file, fieldnames=cal_dict_list[0].keys(), dialect="excel")
        csvwriter.writeheader()
        csvwriter.writerows(cal_dict_list)


def main(calendar_file: TextIO) -> None:
    """main application logic"""
    start_date = (2023, 1, 1)
    end_date = (2023, 1, 31)

    calendar = Calendar.from_ical(calendar_file.read())
    _logger.info("parsing %s", calendar_file.name)
    calendar_file.close()
    new_calendar = x_wr_timezone.to_standard(calendar)
    events = recurring_ical_events.of(new_calendar).between(start_date, end_date)

    for event in events:
        if event["status"] != "CONFIRMED":
            continue

        cal_event = CalendarEvent(event)
        for attendee in cal_event.attendees:
            _contact_list.add(Contact(email=attendee))
        if cal_event.organizer:
            _contact_list.add(Contact(email=cal_event.organizer))
        _calendar_event_list.append(cal_event)
        _logger.debug("added event: %s", cal_event.dict_for_csv())
    save_calendar_list(_calendar_event_list)


# when run as a script, do initialization
if __name__ == "__main__":
    config: Dict[str, Any] = {
        "logfile_name": _LOG_FILE,
        "console_log_level": _CONSOLE_LEVEL,
        "logfile_log_level": _FILE_LEVEL,
        "contacts_file": _CONTACTS_FILE,
    }
    config_parser = load_config_file(config)

    # command-line arguments override config file settings
    arg_parser = argparse.ArgumentParser(description="do something interesting.")
    arg_parser.add_argument("--verbose", "-v", action="store_true", dest="verbose")
    arg_parser.add_argument(
        "--verbose_log", "-V", action="store_true", dest="verbose_log"
    )
    arg_parser.add_argument("calendar_file", type=argparse.FileType("rb"))
    ns = arg_parser.parse_args()
    if ns.verbose:
        config["console_log_level"] = logging.DEBUG
    if ns.verbose_log:
        config["logfile_log_level"] = logging.DEBUG

    initialize_logging(
        config["logfile_name"], config["console_log_level"], config["logfile_log_level"]
    )

    initialize_contact_list(config["contacts_file"])
    main(ns.calendar_file)
    save_contact_list(config["contacts_file"])
