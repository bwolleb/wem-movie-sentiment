import os
import argparse
import json

def loadJson(path):
	f = open(path)
	data = json.load(f)
	f.close()
	return data

def writeJson(data, path):
	w = open(path, "w")
	json.dump(data, w, ensure_ascii=False)
	w.close()

def main():
	parser = argparse.ArgumentParser("Filter movies")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("img", help="Images dir")
	parser.add_argument("sub", help="Subtitles dir")
	parser.add_argument("minYear", help="Min year (inclusive)", type=int)
	parser.add_argument("maxYear", help="Max year (inclusive)", type=int)
	parser.add_argument("output", help="Final file to create")
	args = parser.parse_args()

	movies = loadJson(args.movies)
	filtered = []
	for m in movies:
		uuid = m["uuid"]
		year = m["year"]
		# Check if image exists
		if not os.path.isfile(os.path.join(args.img, uuid)):
			continue
		# Check if subs file exists
		if not os.path.isfile(os.path.join(args.sub, uuid + ".json")):
			continue
		# Check year filter
		if year < args.minYear or year > args.maxYear:
			continue
		# At this point m should be kept
		filtered.append(m)

	print("Kept", len(filtered))
	writeJson(filtered, args.output)

if __name__ == '__main__':
	main()
