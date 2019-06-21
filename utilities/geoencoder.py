import requests


class GeoEncoder:
    def __init__(self, **kwargs):
        self.baseURL = "https://nominatim.openstreetmap.org/?q={}&format={}&limit=1"
        self.default = True
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
        if self.default:
            response = requests.get(
                self.baseURL.format(address, self.format)
            ).json()
            if self.callback is not None:
                return self.callback(response)
            else:
                latlongList = response[0]["boundingbox"]
                latlongList = [float(i) for i in latlongList]
                return (
                    latlongList[1], latlongList[2],
                    latlongList[0], latlongList[3]
                )
        else:
            response = requests.get(self.baseURL)
            return self.callback(response)

    def customParams(self, url, callbackFn):
        if url is not None and callbackFn is not None:
            self.default = False
            self.baseURL = True
            self.callback = callbackFn
