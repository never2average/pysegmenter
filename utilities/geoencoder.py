import requests

baseURL = "https://nominatim.openstreetmap.org/?q={}&format={}&limit=1"


class GeoEncoder:
    def __init__(self, **kwargs):
        if kwargs != {}:
            try:
                self.format = kwargs["format"]
                try:
                    self.callback = kwargs["callback"]
                except Exception:
                    print("callback is a required key word arguement.")
            except Exception:
                print("format is a required key word arguement.")
        else:
            self.format = "json"
            self.callback = None

    def fetchBoundingBox(self, address):
        response = requests.get(baseURL.format(address, self.format)).json()
        if self.callback is not None:
            return self.callback(response)
        else:
            latlongList = response[0]["boundingbox"]
            latlongList = [float(i) for i in latlongList]
            return (
                latlongList[1], latlongList[2],
                latlongList[0], latlongList[3]
            )