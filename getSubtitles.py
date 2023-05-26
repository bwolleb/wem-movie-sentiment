import json
import os
import argparse
import re
import time
import scrapSubs

def main():
	parser = argparse.ArgumentParser("Subtitles downloader")
	parser.add_argument("movies", help="Movies json")
	parser.add_argument("path", help="Where to save images")
	parser.add_argument("--sleep", type=float, required=False, help="TIme to sleep between requests (seconds)", default=0)
	args = parser.parse_args()

	f = open(args.movies)
	movies = json.load(f)
	f.close()

	print("Loaded", len(movies), "movies")
	ok = 0

	for movie in movies:
		srtPath = os.path.join(args.path, movie["uuid"] + ".srt")
		if os.path.isfile(srtPath):
			# Subtitles were already downloaded
			continue
		cleanTitle = re.sub('[^\w ]', '', movie["title"])
		try:
			subs = scrapSubs.getSubtitles(cleanTitle, movie["year"], 1, False)
			if len(subs) > 0:
				w = open(srtPath, "wb")
				w.write(subs)
				w.close()
				ok += 1
				if args.sleep > 0:
					time.sleep(args.sleep)
		except:
			pass
		if ok == 1: break
	print("Downloaded", ok, "on", len(movies))

if __name__ == '__main__':
	main()

