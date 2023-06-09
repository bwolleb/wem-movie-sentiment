import datetime
import os
import argparse
import json
import warnings

tags = ["action", "addiction", "adolescence", "adoption", "adultery", "adventure", "alcohol", "alien", "amnesia", "animal", "animation", "anti hero", "apocalypse", "art", "artificial intelligence", "assassin", "bank", "betrayal", "biography", "business", "car", "casino", "celebrity", "chase", "children", "cinema", "comedy", "coming of age", "computer", "conspiracy", "crime", "cyberpunk", "dance", "dance", "dark comedy", "detective", "disaster", "documentary", "dog", "drama", "drug", "dystopia", "environment", "epic", "espionage", "family", "family drama", "fantasy", "fear", "film noir", "friendship", "future", "gambling", "gangster", "ghost", "gore", "heist", "high school", "historical", "horror", "human rights", "journey", "lgbt", "love", "martial arts", "magic", "mafia", "mental illness", "murder", "music", "musical", "mystery", "nature", "neo-noir", "paranormal", "period drama", "political satire", "politics", "post-apocalyptic", "psychological thriller", "racism", "religion", "romance", "romantic comedy", "satire", "sci-fi", "space", "sports", "spy", "superhero", "supernatural", "survival", "suspense", "terrorism", "thriller", "travel", "vampire", "war", "western", "zombie"]

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
	parser = argparse.ArgumentParser("Compute the dramatic signature on precomputed sentiment analysis")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("subs", help="Subs dir")
	parser.add_argument("output", help="Output json file")
	parser.add_argument("-f", help="From slice", dest="start", type=int, required=False, default=None)
	parser.add_argument("-t", help="To slice", dest="to", type=int, required=False, default=None)
	parser.add_argument("-n", help="Batch size", dest="nb", type=int, required=False, default=8)
	parser.add_argument("-c", help="Cuda device", dest="device", required=False, default="cpu")
	parser.add_argument("-v", help="Verbose", dest="verbose", action="store_true")
	args = parser.parse_args()

	warnings.simplefilter("ignore", UserWarning)
	movies = loadJson(args.movies)
	uuids = [m["uuid"] for m in movies]
	if args.start is not None and args.to is not None:
		uuids = uuids[args.start:args.to]
	uuids = [u for u in uuids if os.path.isfile(os.path.join(args.subs, u + ".json"))]

	# Model
	import torch
	from transformers import pipeline
	device = torch.device(args.device)
	classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

	current = []
	txts = []
	nb = 0
	for u in uuids:
		nb += 1
		current.append(u)
		subs = loadJson(os.path.join(args.subs, u + ".json"))
		txt = [s[2] for s in subs]
		txts.append(txt)
		if len(current) == args.nb or nb == len(uuids):
			if args.verbose: print("Analyzing", len(current), "movies, ", nb, "/", len(uuids))
			res = classifier(txts, tags)
			for i in range(len(current)):
				r = res[i]
				r.pop("sequence")
				writeJson(r, os.path.join(args.output, current[i] + ".json"))
			current = []
			txts = []

if __name__ == '__main__':
	main()
