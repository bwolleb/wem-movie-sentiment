# Visualization
This directory contains the code to run a simple web interface built with `streamlit`. It requires a path to a data folder containing:

	- `movies.json`: the list of all available movies metadata, which is the output of the `01_parser.py` script, possibly filtered by the `06_filterMovies.py` script.
	- `nlp.json`: the NLP data related to the available movies (dramatic signature, tags, stats) which is the combined outputs of the `08_dramaticSignature.py`, `10_getTags.py` and `11_nlpStats.py` scripts.
	- `images`: directory containing the images for each available movie, which is the output of the `02_getImages.py`, possibly cleaned by the `03_removeVideos.py` script.
	- `analysis`: directory containing the detailed sentiment analysis for each available movie, which is the output of the `07_sentimentAnalysis.py` script.

For testing purpose, you can use the `demo` folder containing all the required data for a few movies. The interface should be run like this:

```
streamlit run movie_display.py /path/to/projet/data
```
