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
	parser = argparse.ArgumentParser("Extract most relevant tags from tags analysis")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("tags", help="Tags dir")
	parser.add_argument("output", help="Output file")
	parser.add_argument("-n", help="Top number of tags to extract", dest="top", type=int, required=False, default=3)
	parser.add_argument("-t", help="Threshold for additional tags", dest="thres", type=float, required=False, default=0.1)
	parser.add_argument("-v", help="Verbose", dest="verbose", action="store_true")
	args = parser.parse_args()

	movies = loadJson(args.movies)
	stats = loadJson(args.output) if os.path.isfile(args.output) else {}
	i = 0

	for m in movies:
		i += 1
		uuid = m["uuid"]
		tagsFile = os.path.join(args.tags, uuid + ".json")
		if os.path.isfile(tagsFile):
			analysis = loadJson(tagsFile)
			labels = analysis["labels"]
			scores = analysis["scores"]
			byThres = [labels[i] for i in range(len(labels)) if scores[i] >= args.thres]
			tags = byThres if len(byThres) >= args.top else labels[:args.top]
			if uuid not in stats:
				stats[uuid] = {}
			stats[uuid]["tags"] = tags

	writeJson(stats, args.output)

if __name__ == '__main__':
	main()
