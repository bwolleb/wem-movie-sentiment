import json
import requests
import os
import argparse
import hashlib

baseurl = "https://upload.wikimedia.org/wikipedia/en/{h0}/{h01}/{filename}"
baseurl2 = "https://upload.wikimedia.org/wikipedia/commons/{h0}/{h01}/{filename}"
headers = {}
headers["User-Agent"] = "wem-parser/1.0"

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
		imgPath = os.path.join(args.path, movie["uuid"])
		if "image" in movie and not os.path.isfile(imgPath):
			img = movie["image"]
			if img == "":
				continue
			filename = img.replace(" ", "_")
			chksum = hashlib.md5(filename.encode("utf-8")).hexdigest()
			url = baseurl.format(h0=chksum[0], h01=chksum[:2], filename=filename)
			r = requests.get(url, headers=headers)
			if r.status_code == 200:
				w = open(imgPath, "wb")
				w.write(r.content)
				w.close()
				ok += 1
			elif r.status_code == 404:
				# Try to get it in "commons"
				url = baseurl2.format(h0=chksum[0], h01=chksum[:2], filename=filename)
				r = requests.get(url, headers=headers)
				if r.status_code == 200:
					print("Found in commons")
					w = open(imgPath, "wb")
					w.write(r.content)
					w.close()
					ok += 1
			else:
				print("Request failed", url, r.status_code)
	print("Downloaded", ok, "on", len(movies))

if __name__ == '__main__':
	main()

