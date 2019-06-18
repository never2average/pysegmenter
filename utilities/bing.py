import requests
import shutil
import os


baseURLs = {
    "bing": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/{}%2C{}/{}?mapSize={},{}&format={}&key={}"
}



class ImageFetcher:
    def __init__(self, *args, **kwargs):
        self.zoom = 17
        self. validationError = self._validate_inputs(**kwargs)

    def _validate_inputs(self,**kwargs):
        if len(kwargs.keys()) == 6 or len(kwargs.keys()) == 7:
            if "latitude" in kwargs:
                self.latitude = kwargs["latitude"]
            else:
                print("Key Error: The arguement latitude is a required value")
                return True
            
            if "longitude" in kwargs:
                self.longitude = kwargs["longitude"]
            else:
                print("Key Error: The arguement longitude is a required value")
                return True
            
            if "length" in kwargs:
                self.length = kwargs["length"]
            else:
                print("Key Error: The arguement length is a required value")
                return True
            
            if "breadth" in kwargs:
                self.breadth = kwargs["breadth"]
            else:
                self.breadth = self.length

            if "source" in kwargs:
                self.source = kwargs["source"]
                if not kwargs["source"] in baseURLs:
                    print(
                        "Source Error: Unknown source {}. Available Options are: {}.".format(
                            kwargs["source"], ','.join(baseURLs.keys())
                        )
                    )
                    return True
                else:
                    self.sourceStr = baseURLs[kwargs["source"]]
            else:
                print("Key Error: The arguement source is a required value")
                return True

            if "API_Key" in kwargs:
                self.apikey = kwargs["API_Key"]
            else:
                print("Key Error: The arguement API Key is a required value")
                return True
            
            if "imageType" in kwargs:
                self.imageType = kwargs["imageType"]
            else:
                print("Key Error: The arguement imageType is a required value")
                return True
            return False
        else:
            print(
                "Variable Error: The class requires 6 arguements, you have given {} arguements".format(
                    len(kwargs.keys())
                )
            )
            return False
    
    def fetchImage(self):
        if not self.validationError:
            return self._fetchImage()

    def _fetchImage(self):
        if self.source == "bing":
            print(self.sourceStr.format(
                self.latitude, self.longitude, self.zoom, self.length, self.breadth,
                self.imageType, self.apikey
            ))
            self.image = requests.get(
                self.sourceStr.format(
                    self.latitude, self.longitude, self.zoom, self.length, self.breadth,
                    self.imageType, self.apikey
                ),
                stream=True
            )
            if self.image.status_code == 200:
                self.image.raw.decode_content = True
                print("Image Fetched Successfully")
            else:
                print("Image Fetching Failed")
            return self.image.status_code

    def saveImage(self, dir, filename):
        if not self.validationError:
            return self._saveImage(dir, filename)

    def _saveImage(self, dir, filename):
        if not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except:
                print("Failed to make directory.")
                print("Make sure you are running with appropriate permissions.")
                return "Error"
        
        self.fileAddress = dir+"/"+filename+"."+self.imageType
        with open(self.fileAddress, 'wb') as fobj:
            shutil.copyfileobj(self.image.raw, fobj)
        return "Success"