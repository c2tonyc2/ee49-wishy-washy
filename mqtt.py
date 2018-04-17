from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
from pprint import pprint

TS_READ_KEY = "M6BJ3JTJ7KHYM9J9"
TS_WRITE_KEY = "TQ6PXDYGOSXZV2XA"
TS_CHANNEL_ID = "472546"
API_ENDPOINT = (
    "http://api.thingspeak.com/channels/"
    "{channel_id}/feeds.json?api_key={read_key}"
)
UPDATE_ENDPOINT = "https://api.thingspeak.com/update.json"

def write_ts_data(data):
    """
    @data       dictionary {field<n>: data}
    """
    data["api_key"] = TS_WRITE_KEY
    data = urlencode(data)
    data = data.encode('ascii') # data should be bytes
    req = Request(UPDATE_ENDPOINT, data)

    with urlopen(req) as response:
       the_page = response.read()
       print(the_page)

def read_ts_data():
    """
    Returns data from thingspeak of type bytes.
    """
    with urlopen(
        API_ENDPOINT.format(channel_id=TS_CHANNEL_ID, read_key=TS_READ_KEY)
    ) as response:
        data = response.read()
        pprint(json.loads(data.decode()), width=1)
        return data
