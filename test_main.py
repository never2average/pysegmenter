import pysegmenter
import os


pysegmenter.generateDataset(
	regionName="Bangalore,Karnataka ,India",
	format="png",
	bing_api_key="BING_API_KEY",
	google_api_key="GOOGLE_API_KEY",
	source_option="bing",
	debug=True,
	path=os.path.join(os.getcwd(), "data", "images")
)
