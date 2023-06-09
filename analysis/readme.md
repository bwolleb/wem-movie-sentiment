# Analysis
The scripts in this directories allow to extract movies from a wikipedia dump, download their images, download their english subtitles and perform sentiment analysis, tag analysis and compute NLP stats. The script should be run in order:

- `01_parser.py`: parse a wikipedia dump and extract data for each encountered movie (name, year, cast, plot, image name), creating a UUID for each entry.
- `02_getImages.py`: tries to download the movie images from wikimedia for all parsed entries that have an image.
- `03_removeVideos.py`: cleans the downloaded images directory in order to remove the videos (several old movies are directly inserted as videos of the full film instead of a cover image).
- `04_getSubtitles.py`: tries to download te subtitles for all movies from OpenSubtitles. This script allows to be run multiple times, resuming the operation since the last time because OpenSubtitles quickly blocks automatic requests with a captcha wall.
- `05_srtToJson.py`: converts the scrapped subtitles from their original format "srt" to a structured json.
- `06_filterMovies.py`: filters the movie collection, keeping only those which we could download an image and a subtitle.
- `07_sentimentAnalysis.py`: performs sentiment analysis on the subtitles of all movies. This script uses transformers, which is very slow on CPU but it automatically detects if a CUDA device is available to speed it up (requires appropriate pytorch with cuda package).
- `08_dramaticSignature.py`: computes the dramatic signature, which is a polynomial fit on a given number of degrees.
- `09_extractTags.py`: performs tag extraction from the subtitles. This script uses transformers, which is very slow on CPU but it allows to use a CUDA device, provided in CLI (requires appropriate pytorch with cuda package).
- `10_getTags.py`: extract the most relevant tags (given number, plus a threshold) from the tag extraction.
- `11_nlpStats.py`: performs NLP statistics on the subtitles, like TTR and Flesh's readibility score.
