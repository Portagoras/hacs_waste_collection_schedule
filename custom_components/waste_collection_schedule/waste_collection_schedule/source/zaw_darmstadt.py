from datetime import datetime

import requests
from waste_collection_schedule import Collection

TITLE = "ZAW Darmstadt"  # Title will show up in README.md and info.md
DESCRIPTION = "Source script for waste collection in Darmstadt zaw-online.de"  # Describe your source
URL = "https://zaw-online.de/"  # Insert url to service homepage. URL will show up in README.md and info.md
TEST_CASES = {  # Insert arguments for test cases to be used by test_sources.py script
    "Stresemannstraße": {"street": "Stresemannstraße"},
    "Trondheimstraße": {"street": "Trondheimstraße"},
    "Mühltalstraße": {"street": "Mühltalstraße"},
    "Heinheimer Straße": {"street": "Heinheimer Straße 1-15, 2-16"},
    "Kleyerstraße": {"street": "Kleyerstraße"},
    "Untere Mühlstraße": {"street": "Untere Mühlstraße 1-29, 2-36"},
}

API_URL = "https://zaw.jumomind.com/webservice.php"
ICON_MAP = {  # Optional: Dict of waste types and suitable mdi icons
    "ZAW_REST_W": "mdi:trash-can",
    "ZAW_REST_2W": "mdi:trash-can",
    "ZAW_SCHAD": "mdi:biohazard",
    "ZAW_GELB": "mdi:recycle",
    "ZAW_BIO": "mdi:leaf",
    "ZAW_PAP": "mdi:package-variant",
}

NAME_MAP = {  # Optional: Dict of waste types and suitable mdi icons
    "ZAW_REST_W": "Restmüll",
    "ZAW_REST_2W": "Restmüll (2W)",
    "ZAW_SCHAD": "Schadstoffmobil",
    "ZAW_GELB": "Gelber Sack",
    "ZAW_BIO": "Biomüll",
    "ZAW_PAP": "Papiermüll",
}


class Source:
    def __init__(
        self, city_id, area_id
    ):  # argX correspond to the args dict in the source configuration
        self.city_id = city_id
        self.area_id = area_id

    def fetch(self):
        params = {"idx": "termins", "city_id": self.city_id, "area_id": self.area_id}
        r = requests.get(API_URL, params=params)
        r.raise_for_status()

        schedule = r.json()[0]["_data"]
        if schedule is None or len(schedule) == 0:
            raise Exception("city_id or area_id are invalid")

        entries = []  # List that holds collection schedule
        for entity in schedule:
            entries.append(
                Collection(
                    date=datetime.strptime(
                        entity['cal_date'], "%Y-%m-%d"
                    ).date(),  # Collection date
                    t=NAME_MAP.get(entity['cal_garbage_type']),  # Collection type
                    icon=ICON_MAP.get(entity['cal_garbage_type']),  # Collection icon
                )
            )

        return entries
