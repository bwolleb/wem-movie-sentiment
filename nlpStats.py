import os
import argparse
import json
import nltk
import string
import textstat
import datetime

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
	parser = argparse.ArgumentParser("NLP stats (TTR and Flesch Reading Ease)")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("subs", help="Subs dir")
	parser.add_argument("output", help="Output json file")
	parser.add_argument("-v", help="Verbose", dest="verbose", action="store_true")
	args = parser.parse_args()

	movies = loadJson(args.movies)
	stats = loadJson(args.output) if os.path.isfile(args.output) else {}

	i = 0
	tStart = datetime.datetime.now()
	for m in movies:
		i += 1
		uuid = m["uuid"]
		subsFile = os.path.join(args.subs, uuid + ".json")
		if os.path.isfile(subsFile):
			subs = loadJson(subsFile)
			txt = str.join(" ", [s[2] for s in subs])
			tokens = [w for w in nltk.word_tokenize(txt.lower()) if w not in string.punctuation and not w.isdigit()]
			if uuid not in stats:
				stats[uuid] = {}
			stats[uuid]["ttr"] = len(set(tokens)) / len(tokens)
			stats[uuid]["fre"] = textstat.flesch_reading_ease(txt)
			stats[uuid]["readability"] = textstat.text_standard(txt, float_output=True)
		if args.verbose and i % 100 == 0:
			tNow = datetime.datetime.now()
			secs = (tNow - tStart).total_seconds()
			secsPerFilm = secs / i
			secsRemaining = (len(movies) - i) * secsPerFilm
			hoursRemaining = secsRemaining / 3600
			print("Computed movie", i, "/", len(movies), "seconds per film", secsPerFilm, "remaining", hoursRemaining, "hours")

	writeJson(stats, args.output)

if __name__ == '__main__':
	main()
