import requests
import shutil
import os
from PIL import Image

baseURLs = {
    "bing": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/{},{}/{}?mapSize={},{}&format={}&key={}",
    "googleroad":"http://maps.google.com/maps/api/staticmap?sensor=false&center={},{}&zoom={}&size={}x{}&style=feature:all|element:labels|visibility:off&format={}&key={}",
    "googlesat":"http://maps.google.com/maps/api/staticmap?maptype=satellite&sensor=false&center={},{}&zoom={}&size={}x{}&style=feature:all|element:labels|visibility:off&format={}&key={}"
    }


class ImageFetcher:
    def __init__(self, *args, **kwargs):
        self.zoom = 17
        self.fetchedImage = False
        self.fileSaved = False
        self.validationError = self._validate_inputs(**kwargs)
        

    def _validate_inputs(self, **kwargs):
        if len(kwargs.keys()) in [5, 6, 7, 8]:
            if "point" not in kwargs:
                if "latitude" in kwargs:
                    self.latitude = kwargs["latitude"]
                else:
                    self.pprint(
                        "Key Error: The arguement latitude is required"
                    )
                    return True

                if "longitude" in kwargs:
                    self.longitude = kwargs["longitude"]
                else:
                    self.pprint(
                        "Key Error: The arguement longitude is required"
                    )
                    return True
            else:
                self.latitude = kwargs["point"].y
                self.longitude = kwargs["point"].x

            if "length" in kwargs:
                self.length = kwargs["length"]
            else:
                self.pprint(
                    "Key Error: The arguement length is a required value"
                )
                return True

            if "breadth" in kwargs:
                self.breadth = kwargs["breadth"]
            else:
                self.breadth = self.length

            if "source" in kwargs:
                self.source = kwargs["source"]
                if not kwargs["source"] in baseURLs:
                    self.pprint(
                        "Source Error: Unknown source {}.".format(
                            kwargs["source"]
                        )
                    )
                    self.pprint(
                        "Available Options are: {}.".format(
                            ','.join(baseURLs.keys())
                        )
                    )
                    return True
                else:
                    self.sourceStr = baseURLs[kwargs["source"]]
            else:
                self.pprint(
                    "Key Error: The arguement source is a required value"
                )
                return True

            if "API_Key" in kwargs:
                self.apikey = kwargs["API_Key"]
            else:
                self.pprint(
                    "Key Error: The arguement API Key is a required value"
                )
                return True

            if "imageType" in kwargs:
                self.imageType = kwargs["imageType"]
            else:
                self.pprint(
                    "Key Error: The arguement imageType is a required value"
                )
                return True
            if "debug" in kwargs:
                self.debug = kwargs["debug"]
            else:
                self.debug = False
                return True
            return False
        else:
            self.pprint(
                "Variable Error: The class requires 6 arguements."
            )
            self.pprint(
                "You gave {} arguements".format(len(kwargs.keys()))
            )
            return True

    def fetchImage(self):
        if not self.validationError:
            return self._fetchImage()
        

    def _fetchImage(self):
        if self.source in ["bing","googleroad","googlesat"]:
            self.image = requests.get(
                self.sourceStr.format(
                    self.latitude, self.longitude, self.zoom, self.length,
                    self.breadth, self.imageType, self.apikey
                ),
                stream=True
            )
            if self.image.status_code == 200:
                self.image.raw.decode_content = True
                self.fetchedImage = True
                self.pprint("Image Fetched Successfully")
            else:
                self.pprint("Image Fetching Failed")
            return self.image.status_code

    def saveImage(self, dir, filename):
        if not self.validationError:
            return self._saveImage(dir, filename)

    def _saveImage(self, dir, filename):
        if not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except Exception:
                self.pprint("Failed to make directory.")
                self.pprint("Make sure you have appropriate user privileges.")
                return "Error"
        try:
            self.fileAddress = dir+"/"+filename+"."+self.imageType
            with open(self.fileAddress, 'wb') as fobj:
                shutil.copyfileobj(self.image.raw, fobj)
            self.fileSaved = True
            self.pprint("Image Saved Sucessfully")
            return "Success"
        except Exception:
            self.pprint("Error Occured While Saving Image")
            return "Error"

    def cropImage(self, pixels):
        if self.fetchedImage:
            return self._cropImage(pixels)
        else: print("error 1")

    def _cropImage(self, pixels, **kwargs):
        try:
            if self._checkPathValidity(**kwargs):
                image = Image.open(self.image.raw)
                imageWidth, imageHeight = image.size
                image = image.crop(
                    (pixels, pixels, imageWidth-pixels, imageHeight-pixels)
                )
                self.pprint("Image Cropped Successfully to size {}X{}.".format(
                    imageHeight-2*pixels, imageWidth-2*pixels
                ))
                return "CropSuccess", image
            else:
                self.pprint("An error occured while cropping the Image.")
                return "CropError", Image.new("RGB", (512, 512))
        except Exception:
            self.pprint("An error occured while cropping the Image.")
            return "CropError", Image.new("RGB", (512, 512))

    def _checkPathValidity(self, **kwargs):
        if kwargs == {}:
            return True
        else:
            if "dir" in kwargs:
                if not os.path.isdir(kwargs["dir"]):
                    self.pprint(
                        "The directory provided by you does not exist."
                    )
                    return False
                else:
                    if "filename" in kwargs:
                        self.fileAddress += kwargs["dir"]
                        self.fileAddress += "/"+kwargs["filename"]
                        self.fileAddress += "."+self.imageType
                        return True
                    else:
                        self.pprint("filename is a required attribute.")
                        return False
            else:
                self.pprint("dir is a required attribute.")

    def pprint(self, text):
        if self.debug:
            print(text)
