import shutil
import unittest
import sys
sys.path.insert(1, "..")
from bing import ImageFetcher


class ImageFetcherTest(unittest.TestCase):
    def setUp(self):
        self.imageFetcher = ImageFetcher(
           latitude=42.6564,
           longitude=-73.7638,
           length=576,
           imageType="png",
           source="bing",
           API_Key="YOUR_API_KEY")

    def test_fetch_save_image(self):
        self.assertEqual(200, self.imageFetcher.fetchImage())
        self.assertEqual(
            "Success",
            self.imageFetcher.saveImage("data", "test_image")
        )
        self.assertEqual(
            "Successfully Cropped",
            self.imageFetcher.cropImage(32)
        )

    def tearDown(self):
        shutil.rmtree("data")


if __name__ == '__main__':
    unittest.main()
