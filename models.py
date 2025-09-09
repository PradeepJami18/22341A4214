import datetime

class ClickDetail:
    def __init__(self, timestamp, referrer, location):
        self.timestamp = timestamp
        self.referrer = referrer
        self.location = location

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat() + 'Z',
            "referrer": self.referrer,
            "location": self.location
        }

class URLMapping:
    def __init__(self, original_url, shortcode, validity_minutes):
        self.original_url = original_url
        self.shortcode = shortcode
        self.creation_time = datetime.datetime.now()
        self.validity_minutes = validity_minutes
        self.clicks = []

    def is_expired(self):
        expiry_time = self.creation_time + datetime.timedelta(minutes=self.validity_minutes)
        return datetime.datetime.now() > expiry_time

    def add_click(self, referrer, location):
        click = ClickDetail(datetime.datetime.now(), referrer, location)
        self.clicks.append(click)

    def get_expiry_time(self):
        return self.creation_time + datetime.timedelta(minutes=self.validity_minutes)
