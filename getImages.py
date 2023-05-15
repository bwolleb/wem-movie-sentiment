import json
import requests
import os
import argparse
import hashlib

baseurl = "https://upload.wikimedia.org/wikipedia/en/{h0}/{h01}/{filename}"

def main():
	parser = argparse.ArgumentParser("Wikipedia image extractor")
	parser.add_argument("movies", help="Movies json")
	parser.add_argument("path", help="Where to save images")
	args = parser.parse_args()

	f = open(args.movies)
	movies = json.load(f)
	f.close()

	print("Loaded", len(movies), "movies")
	ok = 0

	for movie in movies:
		if "image" in movie:
			img = movie["image"]
			filename = img.replace(" ", "_")
			chksum = hashlib.md5(filename.encode("utf-8")).hexdigest()
			url = baseurl.format(h0=chksum[0], h01=chksum[:2], filename=filename)
			r = requests.get(url)
			if r.status_code == 200:
				w = open(os.path.join(args.path, movie["uuid"]), "wb")
				w.write(r.content)
				w.close()
				ok += 1
	print("Downloaded", ok, "on", len(movies))

if __name__ == '__main__':
	main()

